import cgi
import facebook
import urllib2
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django_fbi.models import FacebookAccount, FacebookApp
from django_fbi.signals import facebook_connect, facebook_login, facebook_deauthorize
from django_fbi.utils import auth_dialog_url, auth_token_url


class DefaultBackend(object):
    def __init__(self, request):
        self.connect = FacebookApp.objects.connect()
        self.request = request
        self.access_token = None
        self.profile = None
        self.user = None


    def authenticate(self):
        ''' Authenticate the request and return the appropriate user. '''
        if self.profile and self.profile.get('id'):
            self.user = authenticate(facebook_id=self.profile['id'])
        return self.user

    def token_it_up(self):
        ''' Get the access_token and graph profile from ?code. '''
        ## TODO: Better exception handling (although if you Facebook is down, you're pretty much hosed anyways)
        token_url = auth_token_url(self.request, self.request.GET['code'], self.connect)
        data = cgi.parse_qs(urllib2.urlopen(token_url).read())
        self.token = dict([(k, v[0]) for k, v in data.iteritems()]) ## Flatten the data
        graph = facebook.GraphAPI(self.token['access_token'])
        self.profile = graph.get_object('me')


    def next_redirect(self):
        ''' Return an HttpResponseRedirect to the next url. '''
        url = self.request.REQUEST.get('next') or '/'
        return HttpResponseRedirect(url)

    def dialog_redirect(self):
        dialog_url = auth_dialog_url(self.request, self.connect)
        return HttpResponseRedirect(dialog_url)


    def deauthorize_view(self):
        ''' Pinged by Facebook when a user removes the app. '''
        ## Does not play well with Unicode strings.
        data = facebook.parse_signed_request(
            str(self.request.REQUEST['signed_request']),
            str(self.connect['app_secret'])
            )
        account = FacebookAccount.objects.get(facebook_id=data['user_id'])
        account.access_token = None
        account.expires = None
        account.save()
        facebook_deauthorize.send(sender=FacebookAccount, account=account)
        return HttpResponse('OK')

    def connect_view(self):
        ''' Authenticate '''
        if not self.request.GET.get('code'):
            if self.request.user.is_authenticated():
                ## User is auth'd and no ?code, send 'em on their way.
                return self.next_redirect()
            ## No ?code, so we need to authenticate with facebook
            return self.dialog_redirect()
        self.token_it_up() ## Get the access_token and a graph profile from ?code
        self.authenticate()
        if self.request.user.is_authenticated() and not self.user:
            ## The user is authenticated but we don't have a FacebookAccount on record.
            ## Create the account and connect it to our user.
            self.user = request.user
            self.user.facebook = self.create_account()
        if self.user:
            return self.login_user()
        return self.create_user() ## No user, so it's a new registration


    def login_user(self):
        ''' Login the current user. '''
        if not hasattr(self.user, 'backend'):
            self.authenticate()
        login(self.request, self.user)
        self.user.facebook.refresh_profile(self.profile)
        self.user.facebook.access_token = self.token['access_token']
        self.user.facebook.expire_in(self.token['expires']) ## Update the expires time
        self.user.facebook.save()
        facebook_login.send(sender=FacebookAccount, account=self.user.facebook)
        return self.next_redirect()

    def create_user(self):
        ''' Create User+FacebookAccount and login. '''
        self.user = User(
            username='FB_%s' % self.profile['id'],
            first_name=self.profile.get('first_name', ''),
            last_name=self.profile.get('last_name', ''),
            )
        self.user.set_unusable_password()
        self.user.save()
        account = self.create_account()
        facebook_connect.send(sender=FacebookAccount, account=account)
        return self.login_user()

    def create_account(self):
        ''' Create the FacebookAccount object for the current user. '''
        account = FacebookAccount(
            user=self.user,
            facebook_id=self.profile['id'],
            )
        account.save()
        return account
