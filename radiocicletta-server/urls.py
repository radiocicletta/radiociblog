from django.conf.urls.defaults import *
from blog.models import PostsSitemap
from minicms.models import PagesSitemap
from django.views.generic.simple import redirect_to, direct_to_template
from django.conf.urls import *
from django.contrib import admin
handler500 = 'djangotoolbox.errorviews.server_error'
admin.autodiscover()

sitemaps = {
    'posts': PostsSitemap,
    'pages': PagesSitemap,
}

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^admin/blog/report/$', 'blog.admin_views.report'),
    (r'^admin/', include(admin.site.urls)),
    (r'^(?P<id>.*)\.shtml$', redirect_to, {'url': '%(id)s'}),
    (r'^p/', include('profiles.urls')),
    (r'^blog/', include('blog.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^search$', 'google_cse.views.search'),
    (r'robots\.txt$', redirect_to, {'url': '/static/robots.txt'}),
    (r'^favicon\.ico$', redirect_to, {'url': 'http://cdndev.radiocicletta.it/images/favicon.ico'}),
    (r'^listen.pls$', redirect_to, {'url': 'http://radiocicletta.it/listen.pls'}),
    (r'^stream$', redirect_to, {'url': 'http://radiocicletta.it/listen.pls'}),
    (r'^snd/json.xsl$', redirect_to, {'url': 'http://api.radiocicletta.it/snd/json.xsl'}),
    (r'^home/', 'blog.views.oldhome'),
    (r'^$', 'blog.views.oldhome'),
    (r'^programmi(?:/(?P<day>[^/]*))?$', 'blog.views.programmi'),
    (r'^chisiamo/?', 'blog.views.chi'),
    (r'^aiutaci/?', 'blog.views.aiuta'),
    (r'^download/?', 'blog.views.down'),
    (r'^standalone/?', 'blog.views.standalone'),
    (r'^programmi.json', 'programmi.views.progjson'),
    (r'^pro_mob.json', 'programmi.views.modjson'),
    (r'^social.json', 'blog.views.social'),
    (r'^blogs/?', 'blog.views.tuttib'),
    (r'^googleb0d4a078c13a0231.html$', direct_to_template, {'template': 'googleb0d4a078c13a0231.html'})
)
