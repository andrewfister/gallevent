from django.conf.urls import *

#from user_profile.views import UserView

urlpatterns = patterns('user_profile.views',
    url(r'^$', 'show_profile', name='profile'),
	url(r'^groups$', 'show_groups', name='groups'),
	url(r'^posts$', 'show_posts', name='posts'),
	url(r'^datebook$', 'show_datebook', name='datebook'),
)
