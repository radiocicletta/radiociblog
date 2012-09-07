from ..models import Blog
from django.template import Library, Node, Variable
from django.conf import settings
import re
from django.template.defaultfilters import mark_safe

register = Library()

@register.inclusion_tag('blog/feeds.html')
def blog_feeds():
    blogs = Blog.objects.all()
    return {'blogs': blogs}

@register.inclusion_tag('blog/feeds.html')
def blog_feed(blog):
    return {'blogs': (blog,)}

@register.simple_tag
def cdnmediaurl():
    return settings.DISTRIBUITED_CONTENT_URL

@register.filter()
def comicsanitize(value):
    fontregex = re.compile('(?:font(?:-family){0,1})\s*\:[^;]+', re.MULTILINE)
    return mark_safe(fontregex.sub('', value))
