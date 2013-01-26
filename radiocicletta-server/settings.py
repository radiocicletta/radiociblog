# -*- coding: utf-8 -*-

# The following takes care of auto-configuring the database. You might want to
# modify this to match your environment (i.e., without fallbacks).
try:
    from djangoappengine.settings_base import *
    has_djangoappengine = True
except ImportError:
    has_djangoappengine = False
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    # Fall back to MongoDB if App Engine isn't used (note that other backends
    # including SQL should work, too)
    DATABASES = {
        'default': {
            'ENGINE': 'django_mongodb_engine',
            'NAME': 'test',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 27017,
        }
    }

import os

LANGUAGE_CODE='it'
# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'dbindexes'

SITE_NAME = 'radiocicletta-server'
SITE_DESCRIPTION = ''
SITE_COPYRIGHT = ''
DISQUS_SHORTNAME = 'radiocicletta'
GOOGLE_ANALYTICS_ID = 'UA-26545450-1'
GOOGLE_ANALYTICS_DOMAIN = 'radiocicletta.it'
# Get the ID from the CSE "Basics" control panel ("Search engine unique ID")
GOOGLE_CUSTOM_SEARCH_ID = ''
# Set RT username for retweet buttons
TWITTER_USERNAME = 'radiocicletta'
# In order to always have uniform URLs in retweets and FeedBurner we redirect
# any access to URLs that are not in ALLOWED_DOMAINS to the first allowed
# domain. You can have additional domains for testing.
ALLOWED_DOMAINS = ()

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'profiles',
    'urlrouter',
    'minicms',
    'plogo',
    'blog',
    'disqus',
    'djangotoolbox',
    'google_analytics',
    'google_cse',
    'robots',
    'simplesocial',
    'redirects',
    'autoload',
    'dbindexer',
    'permission_backend_nonrel',
    'object_permission_backend_nonrel',
    'programmi',
    'events',
    'replay',
    'authority',

)

if has_djangoappengine:
    # djangoappengine should come last, so it can override a few manage.py commands
    INSTALLED_APPS += ('djangoappengine',)
else:
    INSTALLED_APPS += ('django_mongodb_engine',)


AUTHENTICATION_BACKENDS = (
    'permission_backend_nonrel.backends.NonrelPermissionBackend','object_permission_backend_nonrel.backends.ObjectPermBackend',
)

AUTH_PROFILE_MODULE = 'profiles.UserProfile'


TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

REST_BACKENDS = (
    'minicms.markup_highlight',
    'blog.markup_posts',
)

MIDDLEWARE_CLASSES = (
    'google.appengine.ext.appstats.recording.AppStatsDjangoMiddleware',
    # This loads the index definitions, so it has to come first
    'autoload.middleware.AutoloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'djangotoolbox.middleware.RedirectMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'urlrouter.middleware.URLRouterFallbackMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

CACHE_MIDDLEWARE_SECONDS = 600

URL_ROUTE_HANDLERS = (
    'minicms.urlroutes.PageRoutes',
    'blog.urlroutes.BlogRoutes',
    'blog.urlroutes.BlogPostRoutes',
    'redirects.urlroutes.RedirectRoutes',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'minicms.context_processors.cms'
)

USE_I18N = True

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)



STATICFILES_DIRS = (os.path.join(os.path.dirname(__file__), 'staticstuff'),)
STATIC_ROOT = (os.path.join(os.path.dirname(__file__), 'staticstuff'),)
STATIC_URL = '/static/'


CLOSURE_COMPILER_PATH = os.path.join(os.path.dirname(__file__),
                                     '.webutils', 'compiler.jar')

YUICOMPRESSOR_PATH = os.path.join(os.path.dirname(__file__),
                                  '.webutils', 'yuicompressor.jar')

MEDIA_DEV_MODE = DEBUG
DEV_MEDIA_URL = '/devmedia/'
PRODUCTION_MEDIA_URL = '/media/'

GLOBAL_MEDIA_DIRS = (
    os.path.join(os.path.dirname(__file__), 'static'),
)

#ADMIN_MEDIA_PREFIX = '/media/admin/'

ADMIN_MEDIA_PREFIX ='/media/admin/'
ROOT_URLCONF = 'urls'
#DISTRIBUITED_CONTENT_URL = 'http://localhost:8081'
DISTRIBUITED_CONTENT_URL = 'http://cdndev.radiocicletta.it'

NON_REDIRECTED_PATHS = ('/admin/',)

try:
    from settings_local import *
except ImportError:
    pass
