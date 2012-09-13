from ..models import Blog
from django.template import Library, Node, Variable
from django.conf import settings
import re
from django.template.defaultfilters import mark_safe
from ..smartypants import smartyPants
from ..titlecase import titlecase as tc
from django.core.cache import cache

register = Library()

@register.inclusion_tag('blog/feeds.html')
def blog_feeds():
    blogs = cache.get('blogs')
    if not blogs:
        blogs = Blog.objects.all()
        cache.set('blogs', blogs)
    return {'blogs': blogs}

@register.inclusion_tag('blog/feeds.html')
def blog_feed(blog):
    return {'blogs': (blog,)}

@register.simple_tag
def cdnmediaurl():
    return settings.DISTRIBUITED_CONTENT_URL

fontregex = re.compile('(?:font(?:-family|-size){0,1})\s*\:[^;"]+\;{0,1}\s*', re.MULTILINE)
colorregex = re.compile('(?:color)\s*\:[^;"]+\;{0,1}\s*', re.MULTILINE)
@register.filter
def comicsanitize(value):
    return mark_safe(colorregex.sub('', fontregex.sub('', value)))

@register.filter
def smarty(value): #smartypants
    return mark_safe(smartyPants(value))

@register.filter
def widont(value): #http://shauninman.com/archive/2006/08/22/widont_wordpress_plugin
   return mark_safe(value) 

@register.filter
def titlecase(value):
    return mark_safe(tc(value))
    
