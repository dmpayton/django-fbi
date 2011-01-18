from django.conf.urls.defaults import *

urlpatterns = patterns('django_fbi.views',
   url(r'^connect/$', 'connect', name='connect'),
)
