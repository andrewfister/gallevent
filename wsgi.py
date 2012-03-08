import os
import sys

sys.path.append('/var/www/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'gallevent.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
