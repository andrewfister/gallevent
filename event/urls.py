from django.conf.urls.defaults import *

urlpatterns = patterns('gallevent.event.views',
    (r'^post$', 'post_event'),
    (r'^edit$', 'edit_event'),
)
