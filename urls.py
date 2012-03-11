from django.conf.urls.defaults import *
from django.contrib import admin

from gallevent.map.views import show

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^gallevent/', include('gallevent.foo.urls')),
    (r'^map/', show),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
