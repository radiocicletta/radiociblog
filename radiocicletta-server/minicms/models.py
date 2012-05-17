from django.contrib.sitemaps import Sitemap
from django.db import models
from django import forms
from django.contrib.markup.templatetags import markup

class BaseContent(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True,
        help_text='')
    # This stores the generated HTML code from our wiki syntax
    #pre_rendered_content = models.TextField(blank=True, editable=False)
    pre_rendered_content = models.TextField(blank=True, editable=False)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def rendered_content(self):
        from django.utils.safestring import mark_safe
	#print self.content
        return mark_safe('<div class="userhtml">'+self.content+'</div>')
	#return type(self.pre_rendered_content)
        #context = self.resolve_context(self.context_data)
	#print self.pre_rendered_content
        #return self.pre_rendered_content

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Pre-generate HTML code from our markup for faster access, later
        from .markup import html_body
        self.pre_rendered_content = html_body(self.content)
        super(BaseContent, self).save(*args, **kwargs)

class Page(BaseContent):
    url = models.CharField('URL', max_length=200)
    show_share_buttons = models.BooleanField(default=True,
        help_text='Show buttons for sharing this page on Twitter, Facebook, etc.')
    published = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

class Block(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class PagesSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return Page.objects.filter(published=True)[:2000]

    def lastmod(self, obj):
        return obj.last_update
