from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django_fbi.models import FacebookApp
from facebook import parse_signed_request

def facebook_request(view_func):
    @csrf_exempt
    @never_cache
    def wrapper(request, *args, **kwargs):
        if request.REQUEST.get('signed_request'):
            connect = FacebookApp.objects.connect()
            try:
                data = parse_signed_request(str(request.REQUEST['signed_request']), str(connect.app_secret))
                if not data:
                    data = {}
            except Exception, err:
                data = {}
            request.fbdata = data
        return view_func(request, *args, **kwargs)
    return wrapper
