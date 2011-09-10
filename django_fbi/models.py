import datetime
import facebook
from django.contrib.auth.models import User
from django.db import models
from django.utils import simplejson as json
from django_fbi.managers import FacebookAppManager

class FacebookAccount(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, related_name='facebook')
    facebook_id = models.BigIntegerField(unique=True, db_index=True)
    facebook_email = models.EmailField(max_length=255, blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    profile_data = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('user',)

    def __unicode__(self):
        return unicode(self.facebook_id)

    def graph(self):
        ''' Shortcut to get a GraphAPI object for this account '''
        if not hasattr(self, '_graph'):
            self._graph = facebook.GraphAPI(self.access_token)
        return self.graph
    graph = property(graph)

    def get_profile(self):
        if not hasattr(self, '_profile'):
            self._profile = {}
            if self.profile_data:
                self._profile = json.loads(self.profile_data)
        return self._profile

    def set_profile(self, data):
        self._profile = data
        self.profile_data = json.dumps(data)

    profile = property(get_profile, set_profile)

    def connected(self):
        ''' Determine if we are connected and have an active token. '''
        return self.access_token and not self.is_expired()
    connected = property(connected)

    def is_expired(self):
        ''' Compare self.expires to now to determine if the token has expired. '''
        now = datetime.datetime.utcnow()
        return self.expires > now

    def expire_in(self, seconds):
        ''' Update self.expires to now+seconds. '''
        now = datetime.datetime.utcnow()
        self.expires = now + datetime.timedelta(seconds=int(seconds))

    def refresh_profile(self, profile=None):
        ''' Cache the users /me profile for potential offline use. '''
        if self.access_token and not self.profile:
            try:
                profile = self.graph.get_object('me')
            except facebook.GraphAPIError:
                return False
        if profile:
            profile['image'] = 'https://graph.facebook.com/%s/picture?type=large' % self.facebook_id
            profile['image_thumb'] = 'https://graph.facebook.com/%s/picture' % self.facebook_id
            if profile.get('email'):
                self.facebook_email = profile['email']
            self.profile = profile
            return True
        return False


class FacebookApp(models.Model):
    namespace = models.SlugField(max_length=255)
    connect = models.BooleanField(default=False, help_text='Only one app may be used for Facebook Connect.')
    app_id = models.CharField(max_length=20)
    app_secret = models.CharField(max_length=32)
    scope = models.CharField(max_length=255, blank=True, null=True)
    canvas_template = models.CharField(max_length=255, blank=True, null=True)
    canvas_content = models.TextField(blank=True, null=True)
    tab_template = models.CharField(max_length=255, blank=True, null=True)
    tab_content = models.TextField(blank=True, null=True)

    objects = FacebookAppManager()

    class Meta:
        ordering = ('namespace',)

    def __unicode__(self):
        return unicode(self.namespace)

    def save(self, *args, **kwargs):
        if self.connect:
            ## Only one app may be used for Facebook Connect.
            FacebookApp.objects.exclude(pk=self.pk).update(connect=False)
        super(FacebookApp, self).save(*args, **kwargs)
