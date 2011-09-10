import urllib
from django.conf import settings
from django.core.urlresolvers import reverse
from django_fbi import USE_CONFIGSTORE
from django_fbi.models import FacebookApp

def app_credentials():
    ''' Return the app credentials used for Facebook Connect. '''
    keys = ('app_id', 'app_secret', 'scope')
    if USE_CONFIGSTORE:
        from configstore.configs import get_config
        config = get_config('fb-auth')
        if config:
            return dict([(k, config.get(k)) for k in keys])
    return dict([(k, getattr(settings, 'FACEBOOK_%s' % k.upper(), None)) for k in keys])

def auth_dialog_url(request, connect=None):
    ''' Build the OAuth dialog URL. '''
    if not connect:
        connect = app_credentials()
    dialog_url = 'https://www.facebook.com/dialog/oauth?%s' % urllib.urlencode({
        'client_id': connect['app_id'],
        'scope': connect['scope'],
        'redirect_uri': '%(scheme)s://%(host)s%(path)s' % {
            'scheme': 'https' if request.is_secure() else 'http',
            'host': request.get_host(),
            'path': reverse('fb:connect'),
            'next': request.path
            },
        })
    return dialog_url

def auth_token_url(request, code, connect=None):
    ''' Build the URL where the access_token can be retrieved. '''
    if not connect:
        connect = app_credentials()
    token_url = 'https://graph.facebook.com/oauth/access_token?%s' % urllib.urlencode({
        'client_id': connect['app_id'],
        'client_secret': connect['app_secret'],
        'code': code,
        'redirect_uri': '%(scheme)s://%(host)s%(path)s' % {
            'scheme': 'https' if request.is_secure() else 'http',
            'host': request.get_host(),
            'path': reverse('fb:connect')
            }
        })
    return token_url
