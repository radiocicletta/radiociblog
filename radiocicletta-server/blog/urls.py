from django.conf.urls import *

urlpatterns = patterns('blog.views',
    #(r'^(?P<url>[^/]+)/page/(?P<page>\d+)$', 'browse'),
    (r'^tag/(?P<tag>.*)$', 'tags'),
    (r'^review/(?P<review_key>.*)$', 'review'),
    (r'^blogs/*', 'tuttib'),
    (r'^(?P<blog>[^/]+)/*$', 'browse_blog'),
    (r'^(?P<blog>[^/]+)/(?P<url>[^/]+)/*$', 'get_post'),
)
