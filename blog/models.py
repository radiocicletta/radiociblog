from .utils import slugify
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
from django.db import models
from django.db.models import permalink, CharField, \
    BooleanField, URLField, \
    ForeignKey, DateTimeField, \
    ManyToManyField, SlugField, \
    ImageField
from minicms.models import BaseContent
from random import choice
from string import ascii_letters, digits
from django.core.cache import cache
from programmi.models import Programmi
import math
import re
#from pytz.gae import pytz
import pytz
from redactor.fields import RedactorField
from django_imgur.storage import ImgurStorage

IMGUR = ImgurStorage()


def cache_chunked_get(key):
    """ collecting the chunked keys stored in memcache """
    chunks = cache.get('%s_chunks' % key) or 0
    results = []
    for i in range(0, chunks):
        if cache.get('%s_%d' % (key, i)):
            results.extend(cache.get('%s_%d' % (key, i)))
    return results


def cache_chunked_set(key, value):
    """ preventing the store of more than 1M of data
        under the same memcache key """
    chunksize = 10
    for i in range(0, len(value), chunksize):
        cache.add('%s_%d' % (key, i),
                  value[i: i + chunksize])
    cache.add('%s_chunks' % key,
              int(math.ceil(
                  len(value) / float(chunksize))))

FEEDBURNER_ID = re.compile(r'^http://feeds\d*.feedburner.com/([^/]+)/?$')

tzdata = pytz.timezone('Europe/Rome')


class Blog(models.Model):
    title = CharField(
        max_length=200,
        help_text='This will also be your feed title')

    keywords = CharField(
        max_length=200,
        blank=True,
        help_text='Optional: Add a short'
        ' extra description for the title '
        'tag (for SEO-purposes).')
    url = CharField('URL',
                    max_length=200,
                    help_text='Example: /blog')
    description = CharField(max_length=500,
                            blank=True,
                            help_text='This will also be'
                            ' your feed description.')
    feed_redirect_url = URLField(
        'Feed redirect URL',
        blank=True,
        help_text='Optional (use this to publish feeds via FeedBurner)<br />'
        'Example: http://feeds.feedburner.com/YourFeedBurnerID<br />'
        'If you use FeedBurner this will also enable FeedFlares.')
    default_user = ""
    utenti = ManyToManyField(
        User,
        null=True,
        blank=True,
        help_text='utenti che hanno accesso'
        ' e possono scrivere/modificare questo blog. '
        'Selezionarne almeno uno')
    show = ForeignKey(
        Programmi,
        related_name='programmi',
        default=None,
        blank=True,
        null=True,
        help_text='il programma a cui viene'
        ' associato il blog')
    logo = ImageField(
        upload_to='blogs',
        storage=IMGUR,
        null=True,
        blank=True)

    def __unicode__(self):
        return self.title

    def related_utenti(self):
        return ', '.join([x.username for x in list(self.utenti.all())])

    @property
    def url_prefix(self):
        if self.url.endswith('/'):
            return self.url
        return self.url + '/'

    @property
    def url_stripped(self):
        if self.url.startswith('/'):
            return self.url[1:]
        return self.url

    def feedburner_id(self):
        # Detect FeedBurner ID from feed redirect URL
        match = FEEDBURNER_ID.match(self.feed_redirect_url)
        if match:
            return match.group(1)
        return None

    def get_absolute_url(self):
        return "/blog" + self.url

    def get_feed_url(self):
        return self.feed_redirect_url or self.get_internal_feed_url()

    def get_internal_feed_url(self):
        return self.url_prefix + 'feed/latest'


def default_blog():
    blogs = Blog.objects.all()[:1]
    if blogs:
        return blogs[0]
    return None


def generate_review_key():
    charset = ascii_letters + digits
    return ''.join(choice(charset) for i in range(32))


class Post(BaseContent):
    blog = ForeignKey(Blog, related_name='posts', default=default_blog)
    published = BooleanField(default=False)
    author = ForeignKey(User,
                        related_name='posts',
                        null=True,
                        blank=True,
                        help_text='Optional (filled automatically'
                        ' when saving)')
    #url = CharField('URL',
    url = SlugField('URL',
                    blank=True,
                    unique=True,
                    max_length=200,
                    help_text='Optional (filled automatically'
                    ' when publishing).'
                    ' Better use a hand-optimized URL that is unique and '
                    'SEO-friendly.<br/> Tip: Relative URLs'
                    ' (not starting with "/") will be prefixed '
                    'with the blog\'s URL.')
    published_on = DateTimeField(
        null=True,
        blank=True,
        help_text='Optional (filled automatically when publishing)')
    review_key = CharField(
        max_length=32,
        blank=True,
        help_text='Optional (filled automatically when saving)')
    tags = CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text='Tag separati da virgole')

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        content = RedactorField()
        content.contribute_to_class(Post, 'content')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if not self.published:
            return self.get_review_url()
        return "/blog" + self.url

    @property
    def url_stripped(self):
        return re.sub('^/[^/]*', '', self.url)

    def get_tags(self):
        if self.tags:
            return self.tags.split(',')
        return []

    def get_related_posts(self):
        if not self.tags:
            return []
        posts = Post.objects.all()
        postset = set()
        for tag in re.sub('\s+', '', self.tags).split(','):
            tagged_posts = cache.get('posts_tag_%s' % tag)
            if not tagged_posts:
                tagged_posts = set([i.tags
                                    and tag in i.tags
                                    and i for i in posts])
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
            pattern = re.compile("-[0-9]+$")
            slug = self.blog.url_prefix + slugify(self.title)
            url = pattern.sub("", slug)
            i = 1
            while len(Post.objects.filter(url=url)) > 0:
                url = "%s-%d" % (slug, i)
                i = i + 1
            self.url = url
        elif self.published and not self.url.startswith('/'):
            self.url = self.blog.url_prefix + self.url
        super(Post, self).save(*args, **kwargs)


class PostsSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return Post.objects.filter(
            published=True).order_by('-published_on')[:2000]

    def lastmod(self, obj):
        return obj.last_update
