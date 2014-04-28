from django.conf.urls import *

from user_profile.views import ProfileView

urlpatterns = patterns('user_profile.views',
    url(r'^$', ProfileView.as_view(), name='profile'),
	url(r'^groups$', 'show_groups', name='groups'),
	url(r'^posts$', 'show_posts', name='posts'),
	url(r'^datebook$', 'show_datebook', name='datebook'),
)
