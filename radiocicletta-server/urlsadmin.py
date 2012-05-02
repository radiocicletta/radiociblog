from django.conf.urls.defaults import *
from django.contrib import admin
from django.http import HttpResponse
admin.autodiscover()

def my_view(request): 
	return HttpResponse("Hello!")

def get_admin_urls(urls): 
	def get_urls(): 
		my_urls = patterns('', (r'^my_view/$', admin.site.admin_view(my_view)) ) 
		return my_urls + urls 
	return get_urls

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls



urlpatterns = patterns('',
    (r'', include(admin.site.urls)),
)
