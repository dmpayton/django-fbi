import facebook
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django_fbi.user import FacebookUser

class DefaultBackend(object):
    def __init__(self):
        self.request = None
        self.user = None
        self.facebook = None
        self.facebook_fields = ['facebook_id', 'first_name', 'last_name', 'email']
        self.facebook_fields.extend(getattr(settings, 'FACEBOOK_PROFILE_FIELDS', []))

    def connect(self, request):
        self.request = request
        self.user = self.request.user
        if 'do_login' in self.request.REQUEST:
            self.facebook = self._get_facebook_user()
            if self.facebook.is_authenticated():
                if self.user.is_authenticated():
                    ## User is auth'd with both facebook and us. Connect 'em.
                    return self._connect_user()
                else:
                    self._authenticate_user()
                    if self.user.is_authenticated():
                        ## User is auth'd with facebook and has an account with
                        ## us, but is not currently logged in.
                        return self._login_user()
                    else:
                        try:
                            ## Check to see if there is a none-FB user for this
                            ## email address. If so, display an 'Oops' page.
                            User.objects.get(email=self.facebook.profile['email'])
                            return self._account_conflict()
                        except User.DoesNotExist:
                            ## User does not have an account with us, so create one.
                            return self._register_user()
        return render_to_response('django_fbi/connect.html', {
            }, context_instance=RequestContext(self.request))

    def _get_facebook_user(self):
        '''  '''
        user = facebook.get_user_from_cookie(
            self.request.COOKIES,
            settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_APP_SECRET
            )
        return FacebookUser(user)

    def _get_user_profile(self):
        ''' Shortcut to get the users profile since user.get_profile() may
            throw an error. The default is to create a new profile, but this
            may be overridden in a custom backend. '''
        try:
            return self.user.get_profile()
        except ObjectDoesNotExist:
            app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            UserProfile = get_model(app_label, model_name)
            return UserProfile.objects.create(user=self.user)

    def _next_redirect(self):
        ''' Return an HttpResponseRedirect to the next url '''
        url = self.request.REQUEST.get('next') or '/'
        return HttpResponseRedirect(url)

    def _authenticate_user(self):
        ''' Try to authenticate a user, set self.user if success '''
        kwargs = {'facebook_id': self.facebook.profile['id']}
        if self.facebook.profile.get('email') and self.facebook.profile.get('verified'):
            kwargs['facebook_email'] = self.facebook.profile['email']
        auth_user = authenticate(**kwargs)
        if auth_user:
            self.user = auth_user
        return auth_user

    def _login_user(self, reconnect=False):
        ''' Login the user '''
        login(self.request, self.user)
        if reconnect:
            return self._connect_user()
        return self._next_redirect()

    def _register_user(self):
        ''' Register the user '''
        ## TODO: Build this out using django-registration
        return self._next_redirect()

    def _account_conflict(self):
        return render_to_response('django_fbi/account_conflict.html', {
            }, context_instance=RequestContext(self.request))

    def _connect_user(self):
        ''' Connect the users facebook account to this site. '''
        profile = self._get_user_profile()
        for f in self.facebook_fields:
            if f in self.facebook.profile:
                ## If the attr exists and is not a method, set it.
                if (hasattr(profile, f) and not callable(getattr(profile, f))):
                    try:
                        setattr(profile, f, self.facebook.profile[f])
                    except Exception, err:
                        pass ## TODO: better logging
                if (hasattr(self.user, f) and not callable(getattr(self.user, f))):
                    try:
                        setattr(self.user, f, self.facebook.profile[f])
                    except Exception, err:
                        pass ## TODO: better logging
        self.user.save()
        profile.save()
        return self._next_redirect()
