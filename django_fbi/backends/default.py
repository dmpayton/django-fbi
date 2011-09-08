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
        self.user = authenticate(facebook_id=self.profile.get('uid'))
        return self.user

    def token_it_up(self):
        ''' Get the access_token and graph profile from ?code. '''
        token_url = auth_token_url(self.request, self.request.GET['code'], self.connect)
        data = cgi.parse_qs(urllib2.urlopen(token_url).read())
        self.token = data['access_token'][0]
        graph = facebook.GraphAPI(self.token)
        self.profile = graph.get_object('me')

    def redirect(self):
        ''' Return an HttpResponseRedirect to the next url. '''
        url = self.request.REQUEST.get('next') or '/'
        return HttpResponseRedirect(url)

    def deauthorize_view(self):
        ''' Pinged by Facebook when a user removes the app. '''
        account = FacebookAccount.objects.get(facebook_id=request.fbdata['user_id'])
        account.access_token = None
        account.save()
        facebook_deauthorize.send(sender=FacebookAccount, account=account)
        return HttpResponse('OK')

    def connect_view(self):
        ''' Authenticate '''
        if not self.request.GET.get('code'):
            dialog_url = auth_dialog_url(self.request, self.connect)
            return HttpResponseRedirect(dialog_url)
        self.token_it_up()
        self.authenticate()
        if self.user:
            return self.login_user(refresh_profile=True)
        return self.create_user()

    def login_user(self, refresh_profile=True):
        ''' Login the current user '''
        if not hasattr(self.user, 'backend'):
            self.authenticate()
        login(self.request, self.user)
        if refresh_profile:
            self.user.facebook.refresh_profile()
            self.user.facebook.save()
        facebook_login.send(sender=FacebookAccount, account=self.user.facebook)
        return self.redirect()


    def create_user(self):
        ''' Create the user account and hook it up to the profile. '''
        self.user = User(
            username='FB_%s' % self.profile.get('uid'),
            first_name=self.profile.get('first_name', ''),
            last_name=self.profile.get('last_name', ''),
            )
        self.user.set_unusable_password()
        self.user.save()
        account = FacebookAccount(
            user=self.user,
            facebook_id=self.profile.get('uid'),
            access_token=self.access_token
            )
        account.refresh_profile(self.profile)
        if self.profile['email']:
            account.facebook_email = self.profile['email']
        account.save()
        facebook_connect.send(sender=FacebookAccount, account=account)
        return self.do_login(refresh_profile=False)
