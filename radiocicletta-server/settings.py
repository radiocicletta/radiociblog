# -*- coding: utf-8 -*-

# The following takes care of auto-configuring the database. You might want to
# modify this to match your environment (i.e., without fallbacks).
#try:
#    from djangoappengine.settings_base import *
#except ImportError:
#    DEBUG = True
#    TEMPLATE_DEBUG = DEBUG
#
#    # Fall back to MongoDB if App Engine isn't used (note that other backends
#    # including SQL should work, too)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'blogtransitional', # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}

import os

LANGUAGE_CODE='it'
# Activate django-dbindexer for the default database

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
#    'django_admin_bootstrapped',
    'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'profiles',
    'urlrouter',
    'minicms',
    'plogo',
    'blog',
    'disqus',
    'google_analytics',
    'google_cse',
    'simplesocial',
    'redirects',
    'programmi',
    'events',
    'replay',
    'pytz',
)


#AUTHENTICATION_BACKENDS = (
#    'permission_backend_nonrel.backends.NonrelPermissionBackend','object_permission_backend_nonrel.backends.ObjectPermBackend',
#)

AUTH_PROFILE_MODULE = 'profiles.UserProfile'


REST_BACKENDS = (
#    'minicms.markup_highlight',
    'blog.markup_posts',
)


SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
# #       'BACKEND': 'gae_backends.memcache.MemcacheCache',
#    }
#}

MIDDLEWARE_CLASSES = (
    #'google.appengine.ext.appstats.recording.AppStatsDjangoMiddleware',
    # This loads the index definitions, so it has to come first
    #'autoload.middleware.AutoloadMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'djangotoolbox.middleware.RedirectMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'urlrouter.middleware.URLRouterFallbackMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

CACHE_MIDDLEWARE_SECONDS = 600

URL_ROUTE_HANDLERS = (
#    'minicms.urlroutes.PageRoutes',
    'blog.urlroutes.BlogRoutes',
    'blog.urlroutes.BlogPostRoutes',
    'redirects.urlroutes.RedirectRoutes',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'minicms.context_processors.cms'
)

USE_I18N = True

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)


STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'staticstuff'),
)
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
DISTRIBUITED_CONTENT_URL = 'http://cdn.radiocicletta.it'

NON_REDIRECTED_PATHS = ('/admin/',)

try:
    from settings_local import *
except ImportError:
    pass
