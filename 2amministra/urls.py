from django.conf.urls.defaults import *

urlpatterns = patterns('amministra.views',
    (r'^$', 'index'),
    (r'^postlist','poststable'),
    (r'^test','test'),
)
