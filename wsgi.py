sys.path.append('/var/django/gallevent')
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'gallevent.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
