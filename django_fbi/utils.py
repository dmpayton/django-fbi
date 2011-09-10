import urllib
from django.core.urlresolvers import reverse
from django_fbi.models import FacebookApp

def auth_dialog_url(request, connect=None):
    ''' Build the OAuth dialog URL. '''
    if not connect:
        connect = FacebookApp.objects.connect()
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
        connect = FacebookApp.objects.connect()
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
