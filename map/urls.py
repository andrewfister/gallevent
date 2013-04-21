from django.conf.urls import *

urlpatterns = patterns('gallevent.map.views',
    #Links to views
    (r'^$', 'show'),
)
