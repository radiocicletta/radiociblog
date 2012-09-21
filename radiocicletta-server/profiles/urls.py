from django.conf.urls.defaults import *

urlpatterns = patterns('profiles.views',
    (r'^(p/)?(?P<nickname>[^/]+)/*$', 'show_profile'),
    (r'^p/', 'all_profiles'),
)
