from django.conf.urls.defaults import *
from blog.models import PostsSitemap
from minicms.models import PagesSitemap
from django.views.generic.simple import redirect_to
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
from django.conf import settings
from django.db.models import *
handler500 = 'djangotoolbox.errorviews.server_error'

sitemaps = {
    'posts': PostsSitemap,
    'pages': PagesSitemap,
}


def logout_user(request):
     muser=request.user
     logout(request)
     if(not muser or not muser.is_superuser):
	return HttpResponsePermanentRedirect("/amministra/")
     else:
	return HttpResponsePermanentRedirect("/admin/")
     


urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^admin/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^admin/logout/$', logout_user),
    (r'^admin/', include('urlsadmin')),
    (r'^blog/', include('blog.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',{'sitemaps': sitemaps}),
    (r'^search$', 'google_cse.views.search'),
    (r'^robots\.txt$', 'robots.views.robots'),
    (r'^amministra/*', include('amministra.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^accounts/logout/$','django.contrib.auth.views.logout'),
    (r'^favicon\.ico$',redirect_to, {'url': 'http://radiocicletta-static.appspot.com/images/favicon.ico'}),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^home/', 'blog.views.oldhome'),
    (r'^foto/', 'blog.views.foto'),
    (r'^programmi/', 'blog.views.programmi'),
    (r'^chisiamo/', 'blog.views.chi'),
    (r'^aiutaci/', 'blog.views.aiuta'),
    (r'^download/', 'blog.views.down'),
    (r'^programmi.json', 'programmi.views.progjson'),
    (r'^blogs/', 'blog.views.tuttib'),
)
