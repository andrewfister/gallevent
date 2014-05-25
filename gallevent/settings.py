import os.path

# Django settings for gallevent project.
import local_settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

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

# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = local_settings.STATIC_ROOT_LOCAL

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    local_settings.MEDIA_ROOT_LOCAL,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pubm$v5&ig#6$o*ihd^jqv!z74mh1xqtl_w3^%#ne&hek$@)dg'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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

LOGIN_URL = '/signin/sign_in'
LOGOUT_URL = '/signin/sign_out'

TEMPLATE_DIRS = local_settings.TEMPLATE_DIRS_LOCAL

from mustachejs import conf
conf.conf.MUSTACHEJS_DIRS = local_settings.JSTEMPLATE_DIRS_LOCAL
conf.conf.MUSTACHEJS_APP_DIRNAMES = []

#Include more date formats
USE_L10N = False
TIME_FORMAT = 'g:iA'
DATE_FORMAT = 'm/d/y'

#Some settings for the events
MIN_EVENTS = 10
MAX_EVENTS = 40

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'mustachejs',
    'haystack',
    'map',
    'signin',
    'event',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'logfile':{
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'filename': os.path.join(local_settings.GALLEVENT_PATH, 'logs/gallevent.log'),
        },
        'stream':{
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
            'stream': 'ext://sys.stderr',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'gallevent': {
            'handlers': ['logfile', 'stream'],
            'level': 'DEBUG',
        }
    }
}
