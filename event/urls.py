from django.conf.urls import include, url, patterns

from event.views import PostEventView, EventDetailView, SearchView


urlpatterns = patterns('event.views',
    url(r'^post/?$', PostEventView.as_view(), name='post_event'),
    url(r'^detail/(?P<event_id>\d+)/?$', EventDetailView.as_view(), name='event_detail'),
	url(r'^show/$', 'show_events', name='show_events'),
    url(r'^search/$', SearchView.as_view(), name='search_events'),
)
