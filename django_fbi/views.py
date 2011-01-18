from django.conf import settings
from registration.backends import get_backend

FBI_BACKEND = getattr(settings, 'FBI_BACKEND', 'django_fbi.backends.DefaultBackend')

def connect(request):
    facebook_backend = get_backend(FBI_BACKEND)
    return facebook_backend.connect(request)
