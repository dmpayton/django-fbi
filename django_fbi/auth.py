from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q

class FacebookAuthBackend(ModelBackend):
    def authenticate(self, facebook_id=None):
        try:
            queryset = User.objects.select_related('facebook')
            user = queryset.get(facebook__facebook_id=facebook_id)
        except User.DoesNotExist:
            user = None
        return user
