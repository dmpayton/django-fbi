from django.conf import settings
from django_fbi.utils import get_facebook_settings
from registration.backends import get_backend

FBI_BACKEND = getattr(settings, 'FBI_BACKEND', 'django_fbi.backends.DefaultBackend')

def fbi_context(request):
    app_id, app_secret = get_facebook_settings()
    return {'FACEBOOK_APP_ID': app_id}

def connect(request):
    facebook_backend = get_backend(FBI_BACKEND)
    return facebook_backend.connect(request)
