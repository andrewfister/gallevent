from django.conf.urls import url, patterns

#from gallevent.event.views import EventSearchView
from event.api.resources import EventResource
from event.views import SearchView

event_resource = EventResource()

urlpatterns = patterns('event.views',
    (r'^post/$', 'post_event'),
#    (r'^edit/(?P<event_id>\d+)$', 'edit_event'),
#    (r'^show/$', 'show_events'),
#    (r'^lineup/$', 'show_lineup'),
#    (r'^manage/$', 'manage_events'),
    url(r'^search/$', SearchView.as_view(), name='search_events'),
    #(r'^manage/tickets$', direct_to_template, {'template': 'your-posts-manage-tickets.html'}),
    #(r'^manage/guests$', direct_to_template, {'template': 'your-posts-manage-guests.html'}),
    #(r'^manage/followers$', direct_to_template, {'template': 'your-posts-manage-followers.html'}),
    #(r'^manage/invitations$', direct_to_template, {'template': 'your-posts-manage-invitations.html'}),
    
#    url(r'^events/$', EventSearchView.as_view()),
#    url(r'^events/(?P<id>\d+)', EventSearchView.as_view()),
    
#    url(r'^api/', include(event_resource.urls))
)
