from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from gallevent.event.views import EventSearchView

urlpatterns = patterns('gallevent.event.views',
    (r'^post/$', 'post_event'),
    (r'^edit/(?P<event_id>\d+)$', 'edit_event'),
    (r'^show/$', 'show_events'),
    (r'^lineup/$', 'show_lineup'),
    (r'^manage/$', 'manage_events'),
    (r'^manage/tickets$', direct_to_template, {'template': 'your-posts-manage-tickets.html'}),
    (r'^manage/guests$', direct_to_template, {'template': 'your-posts-manage-guests.html'}),
    (r'^manage/followers$', direct_to_template, {'template': 'your-posts-manage-followers.html'}),
    (r'^manage/invitations$', direct_to_template, {'template': 'your-posts-manage-invitations.html'}),
    
    url(r'^events/$', EventSearchView.as_view()),
    url(r'^events/(?P<id>\d+)', EventSearchView.as_view()),
)
