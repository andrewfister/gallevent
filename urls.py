from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    #Links to views
    (r'^$', 'gallevent.event.views.show_front_page_events'),
    (r'^login/', include('gallevent.login.urls')),
    (r'^event/', include('gallevent.event.urls')),
    (r'^profile/', include('gallevent.user_profile.urls')),
    
    #Static files like css, js, and images
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    
    #Admin page
    (r'^admin/', include(admin.site.urls)),
)
