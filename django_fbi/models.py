import facebook
from django.contrib.auth.models import User
from django.db import models
from django.utils import simplejson as json
from django_fbi.managers import FacebookAppManager

class FacebookAccount(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, related_name='facebook')
    facebook_id = models.BigIntegerField(unique=True)
    facebook_email = models.EmailField(max_length=255, blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    api_data = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('user',)

    def __unicode__(self):
        return unicode(self.facebook_id)

    @property
    def profile(self):
        if not hasattr(self, '_profile'):
            self._profile = {}
            if self.api_data:
                self._profile = json.loads(self.api_data)
        return self._profile

    @profile.setter
    def profile(self, data):
        self._profile = data
        self.api_data = json.dumps(data)

    @property
    def connected(self):
        return bool(self.access_token)

    def refresh_profile(self, profile=None):
        if self.access_token and not self.profile:
            try:
                graph = facebook.GraphAPI(self.access_token)
                profile = graph.get_object('me')
            except facebook.GraphAPIError:
                return False
        if profile:
            profile['image'] = 'https://graph.facebook.com/%s/picture?type=large' % self.facebook_id
            profile['image_thumb'] = 'https://graph.facebook.com/%s/picture' % self.facebook_id
            self.profile = profile
            return True
        return False


class FacebookApp(models.Model):
    namespace = models.SlugField(max_length=255)
    connect = models.BooleanField(default=False, help_text='Only one app may be used for Facebook Connect.')
    app_id = models.CharField(max_length=20)
    app_secret = models.CharField(max_length=32)
    permissions = models.CharField(max_length=255, blank=True, null=True)
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
