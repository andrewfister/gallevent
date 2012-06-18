from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('gallevent.user_profile.views',
    (r'^show$', 'show_profile'),
    (r'^event_prefs$', direct_to_template, {'template': 'your-profile-ep.html'}),
    (r'^profile_form$', direct_to_template, {'template': 'your-profile-form.html'}),
)
