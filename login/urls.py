from django.conf.urls.defaults import *

urlpatterns = patterns('gallevent.login.views',
    (r'^invite_code/$', 'invite_code'),
    (r'^invite_request/$', 'invite_request'),
    (r'^invite_request_received/$', 'invite_request_received'),
    (r'^sign_in/$', 'sign_in'),
    (r'^manage_invites/$', 'manage_invites'),
)
