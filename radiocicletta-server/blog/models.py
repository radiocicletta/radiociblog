from .utils import slugify
from .fields import ModelListField
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
from django.db import models
from django.db.models import permalink
from minicms.models import BaseContent
from random import choice
from string import ascii_letters, digits
from plogo.models import Plogo
from django.core.cache import cache
import re
from pytz.gae import pytz


FEEDBURNER_ID = re.compile(r'^http://feeds\d*.feedburner.com/([^/]+)/?$')

# Alcune soluzioni prese in considerazione per i ManyToManyFields:
# https://bitbucket.org/legutierr/django-manytomany-nonrel/src/881ad974bb42/manytomany/models.py
# https://gist.github.com/1200165
tzdata = pytz.timezone('Europe/Rome')


def cached_blogs():
    b = cache.get('blogs')
    if not b:
        b = Blog.objects.all()
        cache.add('blogs', b)
    return b


def cached_posts():
    p = cache.get('published_posts')
    if not p:
        p = Post.objects.filter(published=True)
        cache.add('published_posts', p)
    return p


def cached_blog_posts(blog):
    p = cache.get('blog_posts_%s' % blog.id)
    if not p:
        p = Post.objects.filter(blog=blog, published=True)
        cache.add('blog_posts_%s' % blog.id, p)
    return p


class Blog(models.Model):
    title = models.CharField(max_length=200,
                             help_text='This will also be your feed title')
    #proprietario = models.CharField(max_length=200,help_text='This will also be your feed title')
    keywords = models.CharField(max_length=200,
                                blank=True,
                                help_text='Optional: Add a short extra description for the title tag (for SEO-purposes).')
    url = models.CharField('URL',
                           max_length=200,
                           help_text='Example: /blog')
    description = models.CharField(max_length=500,
                                   blank=True,
                                   help_text='This will also be your feed description.')
    blog_generic = models.BooleanField(default=False,
                                       help_text='questo blog non &egrave; associato ad alcun programma')
    feed_redirect_url = models.URLField('Feed redirect URL',
                                        verify_exists=False,
                                        blank=True,
                                        help_text='Optional (use this to publish feeds via FeedBurner)<br />'
                                        'Example: http://feeds.feedburner.com/YourFeedBurnerID<br />'
                                        'If you use FeedBurner this will also enable FeedFlares.')
    default_user = ""
    utenti = ModelListField(models.ForeignKey(User,
                                              null=True,
                                              blank=True,
                                              help_text='utenti che hanno accesso e possono scrivere/modificare questo blog. Selezionarne almeno uno'))
    logo = models.ForeignKey(Plogo,
                             related_name='logo',
                             blank=True,
                             null=True)
    mixcloud_playlist = models.CharField('Mixcloud playlist',
                                         max_length=200,
                                         blank=True,
                                         null=True,
                                         help_text='Optional: Add a mixcloud playlist')
    twitter = models.CharField('Account twitter',
                               max_length=200,
                               blank=True,
                               null=True,
                               help_text='Optional: Add a twitter account')
    facebook_page_or_user = models.CharField('Pagina o utente facebook',
                                             max_length=200,
                                             blank=True, null=True,
                                             help_text='Optional: Add a facebook username/page id')

    def __unicode__(self):
        return self.title

    def related_utenti(self):
        return ', '.join([x.username for x in User.objects.filter(id__in=self.utenti)])

    @property
    def url_prefix(self):
        if self.url.endswith('/'):
            return self.url
        return self.url + '/'

    def feedburner_id(self):
        # Detect FeedBurner ID from feed redirect URL
        match = FEEDBURNER_ID.match(self.feed_redirect_url)
        if match:
            return match.group(1)
        return None

    def get_absolute_url(self):
        return self.url

    def get_feed_url(self):
        return self.feed_redirect_url or self.get_internal_feed_url()

    def get_internal_feed_url(self):
        return self.url_prefix + 'feed/latest'

    def get_logo(self):
        try:
            cache_logo = cache.get('blog_%s_logo' % self.pk)
            if not cache_logo:
                cache.set('blog_%s_logo' % self.pk, self.logo)
                return self.logo
            return cache_logo
        except:
            return None


def default_blog():
    blogs = Blog.objects.all()[:1]
    if blogs:
        return blogs[0]
    return None


def generate_review_key():
    charset = ascii_letters + digits
    return ''.join(choice(charset) for i in range(32))


class Post(BaseContent):
    blog = models.ForeignKey(Blog, related_name='posts', default=default_blog)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User,
                               related_name='posts',
                               null=True,
                               blank=True,
                               help_text='Optional (filled automatically when saving)')
    url = models.CharField('URL',
                           blank=True,
                           max_length=200,
                           help_text='Optional (filled automatically when publishing). Better '
                                     'use a hand-optimized URL that is unique and SEO-friendly.<br/>'
                                     'Tip: Relative URLs (not starting with "/") will be prefixed '
                                     "with the blog's URL.")
    published_on = models.DateTimeField(null=True,
                                        blank=True,
                                        help_text='Optional (filled automatically when publishing)')
    review_key = models.CharField(max_length=32,
                                  blank=True,
                                  help_text='Optional (filled automatically when saving)')
    tags = models.CharField(max_length=500,
                            null=True,
                            blank=True,
                            help_text='Tag separati da virgole')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if not self.published:
            return self.get_review_url()
        return self.url

    def get_blog(self):
        cached_blog = cache.get('post_%s_blog' % self.pk)
        if not cached_blog:
            cache.set('post_%s_blog' % self.pk, self.blog)
            return self.blog
        return cached_blog

    def get_tags(self):
        if self.tags:
            return self.tags.split(',')
        return []

    def get_related_posts(self):
        if not self.tags:
            return []
        posts = cached_posts().order_by('-published_on')
        postset = set()
        for tag in re.sub('\s+', '', self.tags).split(','):
            tagged_posts = cache.get('posts_tag_%s' % tag)
            if not tagged_posts:
                tagged_posts = set([i.tags and tag in i.tags and i for i in posts])
                cache.set('posts_tag_%s' % tag, tagged_posts)
            postset.update(tagged_posts)
        try:
            tagged_posts.remove(None)
        except KeyError:
            pass
        try:
            tagged_posts.remove(False)
        except KeyError:
            pass
        try:
            tagged_posts.remove(self)
        except KeyError:
            pass
        return list(postset)[:6]

    def in_blog(self):
        return self.blog.title

    @permalink
    def get_review_url(self):
        return ('blog.views.review', (), {'review_key': self.review_key})

    def save(self, *args, **kwargs):
        if not self.review_key:
            self.review_key = generate_review_key()
        if self.published and not self.published_on:
            self.published_on = tzdata.localize(datetime.now())
        if self.published and not self.url:
            self.url = self.blog.url_prefix + slugify(self.title)
        elif self.published and not self.url.startswith('/'):
            self.url = self.blog.url_prefix + self.url
        super(Post, self).save(*args, **kwargs)


class PostsSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return Post.objects.filter(published=True).order_by('-published_on')[:2000]

    def lastmod(self, obj):
        return obj.last_update
