from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from gallevent.user_profile.views import UserView

urlpatterns = patterns('gallevent.user_profile.views',
    (r'^show$', 'show_profile'),
    (r'^event_prefs$', direct_to_template, {'template': 'your-profile-ep.html'}),
    (r'^profile_form$', direct_to_template, {'template': 'your-profile-form.html'}),
    
    url(r'^user$', UserView.as_view()),
    url(r'^user/(?P<id>\d+)', UserView.as_view()),
)
