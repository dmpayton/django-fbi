import datetime
from django.db import models
from django.db.models import Q


class FacebookAccountManager(models.Manager):
    def connected(self):
        ''' Return a queryset of valid, connected FacebookAccounts '''
        now = datetime.datetime.utcnow()
        queryset = self.exclude(Q(access_token__isnull=True)|Q(access_token__iexact=''))
        queryset = queryset.filter(expires__gt=now, user__active=True)
        return queryset
