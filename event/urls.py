from django.conf.urls import include, url, patterns

#from event.api.resources import EventResource
from event.views import SearchView

#event_resource = EventResource()

urlpatterns = patterns('event.views',
    url(r'^post/$', 'post_event', name='post_event'),
    (r'^edit/(?P<event_id>\d+)$', 'edit_event'),
    (r'^show/$', 'show_events'),
    (r'^lineup/$', 'show_lineup'),
    (r'^manage/$', 'manage_events'),
    url(r'^search/$', SearchView.as_view(), name='search_events'),
#    url(r'^api/', include(event_resource.urls))
)
