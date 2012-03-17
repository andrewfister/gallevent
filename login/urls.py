from django.conf.urls.defaults import *

urlpatterns = patterns('gallevent.login.views',
    (r'^invite_code/$', 'invite_code'),
    (r'^invite_request/$', 'invite_request'),
)
