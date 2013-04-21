from django.conf.urls import *

from user_profile.views import UserView

urlpatterns = patterns('user_profile.views',
    (r'^show$', 'show_profile'),
    #(r'^event_prefs$', direct_to_template, {'template': 'your-profile-ep.html'}),
    #(r'^profile_form$', direct_to_template, {'template': 'your-profile-form.html'}),
    
    url(r'^user$', UserView.as_view()),
    url(r'^user/(?P<id>\d+)', UserView.as_view()),
)
