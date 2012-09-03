from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
    #(r'^(?P<url>[^/]+)/page/(?P<page>\d+)$', 'blog_browse'),
    #(r'^(blog/)?(?P<url>[^/]+)/*$', 'blog_browse'),
    (r'^review/(?P<review_key>.*)$', 'review'),
    (r'^blogs/', 'tuttib'),
)
