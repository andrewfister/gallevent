from django.conf.urls import include,url,patterns
from django.contrib import admin
from django.conf import settings

from event.views import FrontPageView

admin.autodiscover()

urlpatterns = patterns('',
    #Links to views
    url(r'^$', FrontPageView.as_view(), name='front_page'),
    (r'^login/', include('login.urls')),
    (r'^event/', include('event.urls')),
    (r'^profile/', include('user_profile.urls')),
    
    #Static files like css, js, and images
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    
    #Admin page
    (r'^admin/', include(admin.site.urls)),
    
    #haystack search
    (r'^search/', include('haystack.urls')),
)
