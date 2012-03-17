from django.conf.urls.defaults import *

urlpatterns = patterns('gallevent.map.views',
    #Links to views
    (r'^$', 'show'),
)
