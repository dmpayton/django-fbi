from django_fbi.models import FacebookApp

def facebook_app(request):
    try:
        connect = FacebookApp.objects.connect()
        app_id = connect.app_id
        perms = connect.permissions
    except Exception:
        app_id = None
        perms = None
    return {
        'FACEBOOK_APP_ID': app_id,
        'FACEBOOK_PERMISSIONS': perms
        }
