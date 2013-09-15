from django.conf.urls import include,url,patterns
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView

from event.views import FrontPageView

admin.autodiscover()

urlpatterns = patterns('',
    #Links to views
    url(r'^$', FrontPageView.as_view(), name='front_page'),
    url(r'^signin/', include('signin.urls')),
    url(r'^event/', include('event.urls')),
    url(r'^profile/', include('user_profile.urls')),
    
    #Admin page
    url(r'^admin/', include(admin.site.urls)),
    
    #haystack search
    url(r'^search/', include('haystack.urls')),
	
	#Sponsors page
	url('^sponsors.html$', TemplateView.as_view(template_name='sponsors.html', content_type='text/html')),
	
	#About Gallevent page
	url('^about-gallevent.html$', TemplateView.as_view(template_name='about-gallevent.html', content_type='text/html')),
)
