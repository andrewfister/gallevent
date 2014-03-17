from django.conf.urls import include, url, patterns


from event.api.resources import EventResource
from event.views import PostEventView, EventDetailView


urlpatterns = patterns('event.views',
    url(r'^post/?$', PostEventView.as_view(), name='post_event'),
    url(r'^detail/(?P<event_id>\d+)/?$', EventDetailView.as_view(), name='event_detail')
    
#    url(r'^edit/(?P<event_id>\d+)$', PostEventView.as_view(), name='edit_event'),
#    (r'^show/$', 'show_events'),
#    (r'^lineup/$', 'show_lineup'),
#    (r'^manage/$', 'manage_events'),
#    url(r'^search/$', SearchView.as_view(), name='search_events'),
)
