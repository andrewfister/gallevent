from django.conf.urls import url, patterns
from signin import views

urlpatterns = patterns('signin.views',
    url(r'^sign_in/?$', views.SignInView.as_view(), name='sign_in'),
    url(r'^sign_out/?$', views.SignOutView.as_view(), name='sign_out'),
    url(r'^join/?$', views.JoinView.as_view(), name='join'),
)
