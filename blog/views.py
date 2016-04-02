# -*- coding: utf-8 -*-
from .models import Post, Blog
from datetime import datetime, time
from django.contrib.syndication.views import Feed
from django.http import HttpResponse, \
    HttpResponseRedirect, \
    Http404
from django.shortcuts import get_object_or_404, render
from django.utils.feedgenerator import Atom1Feed
from django.core.paginator import Paginator
from simplesocial.api import wide_buttons, narrow_buttons
from config.models import SiteConfiguration
from django.db.models import Q, F
from programmi.models import Programmi
import logging
import json
import pytz

tzdata = pytz.timezone('Europe/Rome')

logger = logging.getLogger(__name__)
config = SiteConfiguration.get_solo()


def social(request):
    result = {'modules': ['mixcloud', 'twitter', 'facebook'],
              'modules_args': {'twitter': {'streams': []},
                               'facebook': {'items': []},
                               'mixcloud': {'username': 'radiocicletta'}}}
    for b in Blog.objects.all():
        if b.show:
            if len(b.show.twitter):
                result['modules_args']['twitter']['streams'].append(
                    b.show.twitter
                )
            if len(b.show.facebook_page_or_user):
                result['modules_args']['facebook']['items'].append(
                    b.show.facebook_page_or_user
                )
    return HttpResponse(json.dumps(result), mimetype='application/json')


### pagine "statiche"
def home(request):
    blogs = Blog.objects.all()
    recent_posts = Post.objects.all()
    recent_posts = recent_posts[:6]
    #TODO: change behaviour using query on config.active_schedule
    today = today_schedule()
    tomorrow = tomorrow_schedule()
    logger.info(datetime.now(tzdata).time())
    current_show = today.filter(
        Q(start_hour__lte=datetime.now(tzdata).time()) &
        Q(end_hour__gte=datetime.now(tzdata).time()) |
        Q(start_hour__lte=datetime.now(tzdata).time()) &
        Q(start_hour__gte=F("end_hour"))
    )
    #TODO: add tomorrow's first show
    next_show = today.filter(
        start_hour__gte=datetime.now(tzdata).time())
    #next_show = [d for d in today
    #             if d.start_hour >= datetime.now(tzdata).time()] + tomorrow[:1]

    return render(
        request, 'blog/index.html',
        {
            'blogs': blogs,
            'recent_posts': recent_posts,
            'today_schedule': today,
            'current_show': current_show.exists() and
            current_show.get() or None,
            'next_show': next_show.exists() and next_show.get() or None,
            'schedule': schedule()
        })


def programmi(request, day=''):
    blogs = Blog.objects.all()
    programmi = Programmi.objects.all()
    return render(request, 'blog/programmi.html',
                  {
                      'blogs': blogs,
                      'programmi': programmi,
                      'today_schedule': today_schedule(),
                      'schedule': schedule(),
                      'rowschedule': orderedschedule()
                  })


def chi(request):
    return render(request, 'blog/chi.html',
                  {'schedule': schedule(),
                   'today_schedule': today_schedule()})


def aiuta(request):
    return render(request, 'blog/aiuta.html',
                  {'schedule': schedule(),
                   'today_schedule': today_schedule()})


def down(request):
    return render(request, 'blog/download.html',
                  {'schedule': schedule(),
                   'today_schedule': today_schedule()})


def standalone(request):
    return render(request, 'blog/standalone.html')


### pagine bloggose
def all_blogs(request):
    blogs = Blog.objects.all()
    recent_posts = Post.objects.all()
    recent_posts = recent_posts[:6]
    return render(request, 'blog/blog.html',
                  {
                      'blogs': blogs,
                      'recent_posts': recent_posts,
                      'today_schedule': today_schedule(),
                      'schedule': schedule()
                  })


def schedule():
    sched = config.active_schedule
    cal = {"lu": ['Lunedi',     0, []],
           "ma": ['Martedi',    1, []],
           "me": ["Mercoledi",  2, []],
           "gi": ["Giovedi",    3, []],
           "ve": ["Venerdi",    4, []],
           "sa": ["Sabato",     5, []],
           "do": ["Domenica",   6, []]}
    for day in cal.keys():
        cal[day][2] = sched.onair.filter(
            start_day=day
        ).order_by('start_hour')

    orderedcal = cal.values()
    orderedcal.sort(lambda x, y: x[1] - y[1])
    return orderedcal


def today_schedule():
    today = datetime.now(tzdata).weekday()
    sched = schedule()
    return sched[today][2]  # Assumendo Lunedi come giorno 0


def tomorrow_schedule():
    today = (datetime.now(tzdata).weekday() + 1) % 7
    sched = schedule()
    return sched[today][2]  # Assumendo Lunedi come giorno 0


def orderedschedule():
    """ Questa funzione restuisce una lista di liste: l'elemento
    calendario[time][day] è un dizionario contenente il titolo, orario
    di inizio e orario di fine del programma che il giorno day va in
    onda all'ora time """

    sched = config.active_schedule
    week = ['lu', 'ma', 'me', 'gi', 've', 'sa', 'do']

    # il calendario è una lista di tanti elementi quando le mezzore
    calendario = [[] for x in range(0, 48)]
    # ogni elemento della lista sarà a sua volta una lista di 7 elementi
    # (quanti i giorni)
    for mezzora in range(0, 48):
        for giorno in xrange(0, 7):
            calendario[mezzora].append(
                sched.onair.filter(
                    start_day=week[giorno],
                    start_hour=time(
                        (mezzora / 2) % 24, (mezzora % 2) * 30)
                ).prefetch_related())
    return calendario


def browse_blog(request, **kwargs):
    blog_id = kwargs.get('blog', None)
    blog = get_object_or_404(Blog, url="/" + blog_id)
    page = abs(int(request.GET.get('page', 1)))
    onair = []
    posts = Post.objects.filter(blog=blog)
    posts = posts
    paged_posts = Paginator(posts, 6).page(page)
    return render(request, 'blog/post_list.html',
                  {
                      'blog': blog,
                      'browse_posts': True,
                      'recent_posts': paged_posts.object_list,
                      'page_obj': paged_posts,
                      'today_schedule': today_schedule(),
                      'schedule': schedule(),
                      'onair': onair
                  })


def get_post(request, **kwargs):
    blog_url = kwargs.get('blog', None)
    post_url = kwargs.get('url', None)
    review = kwargs.get('review', False)
    blog = get_object_or_404(Blog, url="/" + blog_url)
    page = abs(int(request.GET.get('page', 1)))
    post = blog.posts.filter(url="/" + blog_url + "/" + post_url)[0]

    recent_posts = Post.objects.filter(blog=post.blog)[:6]
    return render(request, 'blog/post_detail.html',
                  {
                      'post': post,
                      'blog': post.blog,
                      'recent_posts': recent_posts,
                      'review': review,
                      'today_schedule': today_schedule(),
                      'schedule': schedule()
                  })


def tags(request, tag):
    page = abs(int(request.GET.get('page', 1)))
    posts = Post.objects.all()
    tagged_posts = set([i.tags and tag in i.tags and i for i in posts])
    try:
        tagged_posts.remove(None)
    except KeyError:
        pass
    try:
        tagged_posts.remove(False)
    except KeyError:
        pass
    try:
        tagged_posts.remove('')
    except KeyError:
        pass
    paged_posts = Paginator(list(tagged_posts), 6).page(page)
    return render(request, 'blog/post_tags.html',
                  {
                      'tag': tag,
                      'browse_posts': True,
                      'recent_posts': paged_posts.object_list,
                      'page_obj': paged_posts,
                      'today_schedule': today_schedule(),
                      'schedule': schedule()
                  })


def review(request, review_key):
    post = get_object_or_404(Post, review_key=review_key)
    return render(request, 'blog/post_detail.html',
                  {
                      'post': post,
                      'blog': post.blog,
                      'recent_posts': [],
                      'review': review_key,
                      'today_schedule': today_schedule(),
                      'schedule': schedule()
                  })


def show_post(request, post, review=False):
    logger.warn(post)
    logger.warn(post.blog)
    recent_posts = Post.objects.filter(blog=post.blog)[:6]
    logger.warn(recent_posts)
    return render(request, 'blog/post_detail.html',
                  {
                      'post': post,
                      'blog': post.blog,
                      'recent_posts': recent_posts,
                      'review': review,
                      'today_schedule': today_schedule(),
                      'schedule': schedule()
                  })


def feedburner(feed):
    """Converts a feed into a FeedBurner-aware feed."""
    def _feed(request, blog):
        if not blog.feed_redirect_url or \
                request.META['HTTP_USER_AGENT'].startswith('FeedBurner') or \
                request.GET.get('override-redirect') == '1':
            return feed(request, blog=blog)
        return HttpResponseRedirect(blog.feed_redirect_url)
    return _feed


class LatestEntriesFeed(Feed):
    feed_type = Atom1Feed

    def get_object(self, request, blog):
        return blog

    def title(self, blog):
        return blog.title

    def link(self, blog):
        return blog.get_absolute_url()

    def subtitle(self, blog):
        return blog.description

    def item_title(self, post):
        return post.title

    def item_description(self, post):
        url = 'http%s://%s%s' % ('s' if self._request.is_secure() else '',
                                 self._request.get_host(),
                                 post.get_absolute_url())
        header = wide_buttons(
            self._request, post.title, post.get_absolute_url())
        footer = narrow_buttons(
            self._request, post.title, post.get_absolute_url())
        footer += '<p><a href="%s#disqus_thread">Leave a comment</a></p>' % url
        return header + post.rendered_content + footer

    def item_author_name(self, post):
        return post.author.get_full_name()

    def item_pubdate(self, post):
        return post.published_on

    def items(self, blog):
        query = Post.objects.filter(blog=blog)
        # TODO: add select_related('author') once it's supported
        return query[:100]


@feedburner
def latest_entries_feed(request, *args, **kwargs):
    feed = LatestEntriesFeed()
    feed._request = request
    return feed(request, *args, **kwargs)
