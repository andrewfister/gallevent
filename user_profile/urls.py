from django.conf.urls.defaults import *

urlpatterns = patterns('gallevent.user_profile.views',
    (r'^show$', 'show_profile'),
)
