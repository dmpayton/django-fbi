import facebook
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


class DefaultBackend(object):
    def __init__(self, request):
        connect = FacebookApp.objects.connect()
        self.FACEBOOK_APP_ID = connect.app_id
        self.FACEBOOK_APP_SECRET = connect.app_secret
        self.request = request
        self.facebook = None
        self.user = None

    def authenticate(self, facebook_id=None, facebook_email=None):
        self.facebook = facebook.get_user_from_cookie(
            self.request.COOKIES,
            self.FACEBOOK_APP_ID,
            self.FACEBOOK_APP_SECRET
            )
        self.user = authenticate(facebook_id=self.facebook['uid'])
        return self.user

    def redirect(self):
        ''' Return an HttpResponseRedirect to the next url '''
        url = self.request.REQUEST.get('next') or '/'
        return HttpResponseRedirect(url)

    def deauthorize(self):
        ''' Pinged by Facebook when a user removes the app. '''
        account = FacebookAccount.objects.get(facebook_id=request.fbdata['user_id'])
        account.access_token = None
        account.connected = False
        account.save()
        facebook_deauthorize.send(sender=FacebookAccount, account=account)
        return HttpResponse('OK')

    def connect(self):
        ''' Authenticate '''
        self.authenticate()
        if self.user:
            return self.do_login()
        return self.do_connect()

    def do_login(self, refresh_profile=True):
        ''' Login the current user '''
        if not hasattr(self.user, 'backend'):
            self.authenticate()
        login(self.request, self.user)
        if refresh_profile:
            self.user.facebook.refresh_profile()
            self.user.facebook.save()
        facebook_login.send(sender=FacebookAccount, account=user.facebook)
        return self.redirect()

    def do_connect(self):
        ''' Create the user account and hook it up to the profile '''
        graph = facebook.GraphAPI(self.facebook['access_token'])
        fbuser = graph.get_object('me')
        self.user = User(
            username='FB_%s' % self.facebook['uid'],
            first_name=fbuser.get('first_name', ''),
            last_name=fbuser.get('last_name', ''),
            )
        self.user.set_unusable_password()
        self.user.save()
        account = FacebookAccount(
            user=self.user,
            facebook_id=self.facebook['uid'],
            access_token=self.facebook['access_token']
            )
        account.refresh_profile(fbuser)
        if fbuser['email']:
            account.facebook_email = fbuser['email']
        account.save()
        facebook_connect.send(sender=FacebookAccount, account=account)
        return self.do_login(refresh_profile=False)
