from django.conf.urls.defaults import *

urlpatterns = patterns('django_fbi.views',
    url(r'^connect/$', 'connect', name='connect'),
    url(r'^deauthorize/$', 'deauthorize', name='deauthorize'),
    url(r'^app/(?P<slug>[-\w]+)/$', 'view_app', {'page': 'canvas'}, name='canvas'),
    url(r'^app/(?P<slug>[-\w]+)/tab/$', 'view_app', {'page': 'tab'}, name='tab'),
)
