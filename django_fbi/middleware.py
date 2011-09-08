from django.core.exceptions import ImproperlyConfigured
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

class FacebookConnectMiddleware(object):
    def process_request(self, request):
        from django_fbi.models import FacebookApp
        _thread_locals.request = request
        try:
            _thread_locals.connect = FacebookApp.objects.connect()
        except ImproperlyConfigured:
            pass

    def process_response(self, request, response):
        try:
            del _thread_locals.request
        except AttributeError:
            pass
        try:
            del _thread_locals.connect
        except AttributeError:
            pass
        return response
