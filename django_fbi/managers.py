from django.core.exceptions import ImproperlyConfigured
from django.db import models

class FacebookAppManager(models.Manager):
    def connect(self):
        try:
            return self.model.objects.get(connect=True)
        except (self.model.DoesNotExist):
            raise ImproperlyConfigured('No Facebook app is setup for Connect.')
        except (self.model.MultipleObjectsReturned):
            raise ImproperlyConfigured('Multiple Facebook apps are setup for Connect.')
