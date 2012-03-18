from django.conf.urls.defaults import *

urlpatterns = patterns('gallevent.event.views',
    (r'^post/$', 'post_event'),
    (r'^edit/$', 'edit_event'),
    (r'^show/$', 'show_events'),
    (r'^lineup/$', 'show_lineup'),
    (r'^manage/$', 'manage_events'),
)