# Django settings for gallevent project.
import local_settings
import django

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import logging
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
    filename = '/tmp/gallevent.log',
    filemode = 'w'
)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'galleventdb',
        'USER': 'galleventdbadmin',
        'PASSWORD': 'oreborestore',
        'HOST': local_settings.DATABASE_HOST_LOCAL,
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': local_settings.HAYSTACK_HOST_LOCAL + ':9200/',
        'INDEX_NAME': 'haystack',
    },
}

HAYSTACK_DEFAULT_OPERATOR = 'AND'

#HAYSTACK_SITECONF = 'gallevent.search_sites'
#HAYSTACK_SEARCH_ENGINE = 'solr'
#HAYSTACK_SOLR_URL = local_settings.HAYSTACK_HOST_LOCAL + ':8983/solr'
#HAYSTACK_INCLUDE_SPELLING = False
#HAYSTACK_SEARCH_RESULTS_PER_PAGE = 30


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = local_settings.MEDIA_ROOT_LOCAL

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pubm$v5&ig#6$o*ihd^jqv!z74mh1xqtl_w3^%#ne&hek$@)dg'

# List of callables that know how to import templates from various sources.
if django.VERSION[1] == 3:
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.load_template_source',
        'django.template.loaders.app_directories.load_template_source',
    )
elif django.VERSION[1] == 4:
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'gallevent.urls'

LOGIN_URL = '/login/sign_in'
LOGOUT_URL = '/login/sign_out'

TEMPLATE_DIRS = local_settings.TEMPLATE_DIRS_LOCAL

from mustachejs import conf
conf.conf.MUSTACHEJS_DIRS = local_settings.JSTEMPLATE_DIRS_LOCAL
conf.conf.MUSTACHEJS_APP_DIRNAMES = []

#Include more date formats
USE_L10N = False
TIME_FORMAT = 'g:iA'
DATE_FORMAT = 'm/d/y'

#Some settings for the events
MAX_EVENTS = 50

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'mustachejs',
    'haystack',
    'tastypie',
    'map',
    'login',
    'event',
)
