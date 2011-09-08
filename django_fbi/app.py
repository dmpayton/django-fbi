
class FacebookApp(object):
    def canvas_view(self, request):
        raise NotImplemented

    def tab_view(self, request):
        raise NotImplemented

class AppRegistry(dict):
    def register(self, app):
        if not isinstance(app, FacebookApp):
            raise TypeError('App must be an instance of django_fbi.app.FacebookApp')
        if not app.namespace:
            raise AttributeError('Namespace not set on FacebookApp')
        if app.namespace in self._registry:
            raise ValueError('App with namespace "%s" already registered' % app.namespace)
        self[app.namespace] = app

    def unregister(self, app_or_namespace):
        try:
            if isinstance(app_or_namespace, FacebookApp):
                del self[app_or_namespace.namespace]
                return True
            elif isinstance(app_or_namespace, basestring):
                del self[app_or_namespace]
                return True
        except KeyError:
            pass
        return False

apps = AppRegistry()
