from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('gallevent.event.views',
    (r'^post/$', 'post_event'),
    (r'^edit/$', 'edit_event'),
    (r'^show/$', 'show_events'),
    (r'^lineup/$', 'show_lineup'),
    (r'^manage/$', 'manage_events'),
    (r'^manage/tickets$', direct_to_template, {'template': 'your-posts-manage-tickets.html'}),
    (r'^manage/rsvps$', direct_to_template, {'template': 'your-posts-manage-rsvps.html'}),
    (r'^manage/followers$', direct_to_template, {'template': 'your-posts-manage-followers.html'}),
    (r'^manage/invitations$', direct_to_template, {'template': 'your-posts-manage-invitations.html'}),
)
