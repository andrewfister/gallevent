from django.conf.urls import *

#from user_profile.views import UserView

urlpatterns = patterns('user_profile.views',
    (r'^$', 'show_profile'),
	(r'^datebook$', 'show_datebook'),
)
