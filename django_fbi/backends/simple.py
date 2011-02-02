from django.contrib.auth.models import User
from django_fbi.backends.default import DefaultBackend

class SimpleBackend(DefaultBackend):
    def _register_user(self):
        ''' Simple registration for sites that use email for auth. Users are
            created with the username "FB_<facebook_id>", logged in, and
            redirected. Requires 'email' permission from Facebook.
        '''
        self.user = User(
            username='FB_%s' % self.facebook.profile['id'],
            email=self.facebook.profile['email']
            )
        self.user.set_unusable_password()
        self.user.save()
        profile = self._get_user_profile()
        profile.facebook_id = self.facebook.profile['id']
        profile.facebook_email = self.facebook.profile['email']
        profile.save()
        self._authenticate_user() ## need a User object with .backend
        return self._login_user(reconnect=True)
