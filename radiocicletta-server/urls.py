from django.conf.urls.defaults import *
from blog.models import PostsSitemap
from minicms.models import PagesSitemap
from django.views.generic.simple import redirect_to
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
from django.conf import settings
from django.db.models import *
#from django.conf.urls import patterns, url, include
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
    (r'^p/', include('profiles.urls')),
    (r'^blog/', include('blog.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',{'sitemaps': sitemaps}),
    (r'^search$', 'google_cse.views.search'),
    (r'^robots\.txt$', 'robots.views.robots'),
    (r'^favicon\.ico$',redirect_to, {'url': 'http://cdn.radiocicletta.it/images/favicon.ico'}),
    (r'^listen.pls$',redirect_to, {'url': 'http://radiocicletta.it/listen.pls'}),
    (r'^stream$',redirect_to, {'url': 'http://radiocicletta.it/listen.pls'}),
    (r'^home/', 'blog.views.oldhome'),
    (r'^$', 'blog.views.oldhome'),
    (r'^foto/', 'blog.views.foto'),
    #(r'^programmi/', 'blog.views.programmi'),
    (r'^programmi/(?P<day>[^/]*)/*$', 'blog.views.programmi'),
    (r'^chisiamo/', 'blog.views.chi'),
    (r'^aiutaci/', 'blog.views.aiuta'),
    (r'^download/', 'blog.views.down'),
    (r'^standalone/', 'blog.views.standalone'),
    (r'^programmi.json', 'programmi.views.progjson'),
    (r'^pro_mob.json', 'programmi.views.modjson'),
    (r'^social.json', 'blog.views.social'),
    (r'^blogs/', 'blog.views.tuttib'),

)
