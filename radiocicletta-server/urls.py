from blog.models import PostsSitemap
from minicms.models import PagesSitemap
#from django.views.generic.simple import redirect_to, direct_to_template
from django.views.generic.base import TemplateView, RedirectView
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
    (r'^(?P<id>.*)\.shtml$', RedirectView.as_view(url='%(id)s')),
    (r'^p/', include('profiles.urls')),
    (r'^blog/', include('blog.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^search$', 'google_cse.views.search'),
    (r'robots\.txt$', RedirectView.as_view(url='/static/robots.txt')),
    (r'^favicon\.ico$', RedirectView.as_view(url='http://cdn.radiocicletta.it/images/favicon.ico')),
    (r'^listen.pls$', RedirectView.as_view(url='http://radiocicletta.it/listen.pls')),
    (r'^stream$', RedirectView.as_view(url='http://radiocicletta.it/listen.pls')),
    (r'^snd/json.xsl$', RedirectView.as_view(url='http://api.radiocicletta.it/snd/json.xsl')),
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
    (r'^googleb0d4a078c13a0231.html$', TemplateView.as_view(template_name='googleb0d4a078c13a0231.html'))
)
