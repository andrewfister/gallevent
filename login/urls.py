from django.conf.urls import url, patterns
from login import views

urlpatterns = patterns('login.views',
    url(r'^sign_in/$', views.SignInView.as_view(), name='sign_in'),
    url(r'^sign_out/$', views.SignOutView.as_view(), name='sign_out'),
)
