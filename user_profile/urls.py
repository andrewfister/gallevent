from django.conf.urls import *

from user_profile.views import ProfileView, PostsView

urlpatterns = patterns('user_profile.views',
                       url(r'^$', ProfileView.as_view(), name='profile'),
                       url(r'^groups$', 'show_groups', name='groups'),
                       url(r'^posts$', PostsView.as_view(), name='posts'),
                       url(r'^datebook$', 'show_datebook', name='datebook'),
                       )
