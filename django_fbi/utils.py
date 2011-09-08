import urllib
from django.core.urlresolvers import reverse
from django_fbi.models import FacebookApp

def auth_dialog_url(request, connect=None):
    if not connect:
        connect = FacebookApp.objects.connect()
    return 'https://www.facebook.com/dialog/oauth?%s' % urllib.urlencode({
                'client_id': connect['app_id'],
                'redirect_uri': '%(scheme)s://%(host)s%(path)s' % {
                    'scheme': 'https' if request.is_secure() else 'http',
                    'host': request.get_host(),
                    'path': reverse('fb:connect')
                    }
                })

def auth_token_url(request, code, connect=None):
    if not connect:
        connect = FacebookApp.objects.connect()
    return 'https://graph.facebook.com/oauth/access_token?%s' % urllib.urlencode({
                'client_id': connect['app_id'],
                'client_secret': connect['app_secret'],
                'code': code,
                'redirect_uri': '%(scheme)s://%(host)s%(path)s' % {
                    'scheme': 'https' if request.is_secure() else 'http',
                    'host': request.get_host(),
                    'path': reverse('fb:connect')
                    }
                })
