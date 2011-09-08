import urllib
from django_fbi.models import FacebookApp
from django_fbi.utils import auth_dialog_url

def facebook_app(request):
    try:
        connect = FacebookApp.objects.connect()
        context = {
            'FACEBOOK_APP_ID': connect['app_id'],
            'FACEBOOK_AUTH_SCOPE': connect['scope'],
            'FACEBOOK_AUTH_URL': auth_dialog_url(request)
            }
    except Exception, err:
        print err
        context = {
            'FACEBOOK_APP_ID': None,
            'FACEBOOK_AUTH_SCOPE': None,
            'FACEBOOK_AUTH_URL': None,
            }
    return context
