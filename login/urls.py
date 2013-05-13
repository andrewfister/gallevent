from django.conf.urls import url, patterns
from login import views

urlpatterns = patterns('login.views',
    (r'^invite_code/$', 'invite_code'),
    (r'^invite_request/$', 'invite_request'),
    (r'^invite_request_received/$', 'invite_request_received'),
    url(r'^sign_in/$', views.SignInView.as_view(), name='sign_in'),
    (r'^sign_out/$', 'sign_out'),
    (r'^manage_invites/$', 'manage_invites'),
)
