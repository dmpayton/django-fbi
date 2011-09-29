from django.conf.urls.defaults import *

urlpatterns = patterns('django_fbi.views',
    url(r'^channel/$', 'channel', name='channel'),
    url(r'^connect/$', 'connect', name='connect'),
    )
