from ..models import Blog
from django.template import Library
from django.conf import settings
from django.template.defaultfilters import mark_safe
from ..smartypants import smartyPants
from ..titlecase import titlecase as tc
from django.core.cache import cache
import re

register = Library()


@register.inclusion_tag('blog/feeds.html')
def blog_feeds():
    blogs = cache.get('blogs')
    if not blogs:
        blogs = Blog.objects.all()
        cache.set('blogs', list(blogs))
    return {'blogs': blogs}


@register.inclusion_tag('blog/feeds.html')
def blog_feed(blog):
    return {'blogs': (blog,)}


@register.simple_tag
def cdnmediaurl():
    return settings.DISTRIBUITED_CONTENT_URL


@register.simple_tag
def cdnmediaurljs():
    return settings.DISTRIBUITED_CONTENT_URL.replace("/", "\/")

fonttagregex = re.compile('</{0,1}font[^>]*>')
fontregex = re.compile('(?:font(?:-family|-size){0,1})\s*\:[^;"]+\;{0,1}\s*', re.MULTILINE)
colorregex = re.compile('(?:color)\s*\:[^;"]+\;{0,1}\s*', re.MULTILINE)
styleregex = re.compile('style="[^"]*"', re.MULTILINE)
#imageregex = re.compile('(<img [^>]*>)', re.MULTILINE)
srcregex = re.compile('<(\w+[^>]+)src', re.MULTILINE | re.IGNORECASE)


@register.filter
def comicsanitize(value):
    return mark_safe(colorregex.sub('', fontregex.sub('', fonttagregex.sub('', value))))
    #return mark_safe(colorregex.sub('', fontregex.sub('', value)))


@register.filter
def smarty(value):  # smartypants
    return mark_safe(smartyPants(value))


@register.filter
def widont(value):  # http://shauninman.com/archive/2006/08/22/widont_wordpress_plugin
    return mark_safe(value)


@register.filter
def rewritesrc(value):
    return mark_safe(srcregex.sub('<\g<1>data-src', styleregex.sub('', value)))


@register.filter
def titlecase(value):
    return mark_safe(tc(value))
