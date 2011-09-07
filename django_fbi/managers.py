from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django_fbi.middleware import _thread_locals

class FacebookAppManager(models.Manager):
    def connect(self):
        try:
            ## If we're in a request/response cycle and the middleware
            ## is installed, we should already have the app.
            return _thread_locals.connect
        except AttributeError:
            ## It's not cached in _thread_locals, look it up.
            try:
                return self.model.objects.get(connect=True)
            except (self.model.DoesNotExist):
                raise ImproperlyConfigured('No Facebook app is setup for Connect.')
            except (self.model.MultipleObjectsReturned):
                raise ImproperlyConfigured('Multiple Facebook apps are setup for Connect.')
