from .models import Blog, Post, cached_blogs, cached_posts, cached_blog_posts
from datetime import datetime, time
from django.contrib.syndication.views import Feed
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.utils.feedgenerator import Atom1Feed
from django.core.paginator import Paginator
from simplesocial.api import wide_buttons, narrow_buttons
from programmi.models import Programmi
from django.core.cache import cache
import logging
try:
    import simplejson as json
except:
    import json
from pytz.gae import pytz

tzdata = pytz.timezone('Europe/Rome')

logger = logging.getLogger(__name__)


def cached_programmi():
    p = cache.get('programmi')
    if not p:
        p = Programmi.objects.all()
        cache.add('programmi', p)
    return p


def cached_onair(blog):

    onair = cache.get('cached_onair_%s' % blog.id)
    if onair:
        return onair

    onair = []
    try:
        onair = [{'startgiorno': p.startgiorno, 'startora': p.startora} for p in cached_programmi().filter(blog=blog)]
    except:
        pass
    for p in onair:
        p['startgiorno'] = {'lu': 'Lunedi',
                            'ma': 'Martedi',
                            'me': 'Mercoledi',
                            'gi': 'Giovedi',
                            've': 'Venerdi',
                            'sa': 'Sabato',
                            'do': 'Domenica'}[p['startgiorno']]
    cache.set('cached_onair_%s' % blog.id, onair)
    return onair


def social(request):
    result = {'modules': ['mixcloud', 'twitter', 'facebook'],
              'modules_args': {'twitter': {'streams': []},
                               'facebook': {'items': []},
                               'mixcloud': {'username': 'radiocicletta'}}}
    for b in cached_blogs():
        if len(b.twitter):
            result['modules_args']['twitter']['streams'].append(b.twitter)
        if len(b.facebook_page_or_user):
            result['modules_args']['facebook']['items'].append(b.facebook_page_or_user)
    return HttpResponse(json.dumps(result), mimetype='application/json')


### pagine "statiche"
def oldhome(request):
    blogs = cached_blogs()
    recent_posts = cached_posts()
    recent_posts = recent_posts.order_by('-published_on')[:6]
    today = today_schedule()
    tomorrow = tomorrow_schedule()
    logger.info(datetime.now(tzdata).time())
    current_show = [d for d in today
                    if d.startora <= datetime.now(tzdata).time()
                    and d.endora >= datetime.now(tzdata).time()
                    or d.startora <= datetime.now(tzdata).time()
                    and d.startora >= d.endora]
    next_show = [d for d in today if d.startora >= datetime.now(tzdata).time()] +  tomorrow[:1]

                                 #and d.endora >= datetime.now(tzdata).time()]

    return render(request, 'blog/index.html',
                  {'blogs': blogs,
                   'recent_posts': recent_posts,
                   'today_schedule': today,
                   'current_show': current_show and current_show[0] or current_show,
                   'next_show': next_show and next_show[0] or next_show,
                   'schedule': schedule()})


def foto(request):
    return render(request, 'blog/foto.html',
                  {'schedule': schedule(),
                   'today_schedule': today_schedule()})


def programmi(request, day=''):
    blogs = cached_blogs()
    if str(day)[:2].lower() in ['lu', 'ma', 'me', 'gi', 've', 'sa', 'do']:
        # stiamo scherzando?
        programmi = set(cached_programmi().filter(
                        startgiorno=day[:2].lower())).union(
                            set(cached_programmi().filter(
                                endgiorno=day[:2].lower())))
        return render(request, 'blog/programmiday.html',
                      {'blogs': blogs,
                       'programmi': programmi,
                       'today_schedule': today_schedule(),
                       'schedule': schedule(),
                       'rowschedule': orderedschedule()})

    programmi = cached_programmi()
    return render(request, 'blog/programmi.html',
                  {'blogs': blogs,
                   'programmi': programmi,
                   'today_schedule': today_schedule(),
                   'schedule': schedule(),
                   'rowschedule': orderedschedule()})


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
def tuttib(request):
    blogs = cached_blogs()
    recent_posts = cached_posts()
    recent_posts = recent_posts.order_by('-published_on')[:6]
    return render(request, 'blog/blog.html',
                  {'blogs': blogs,
                   'recent_posts': recent_posts,
                   'today_schedule': today_schedule(),
                   'schedule': schedule()})


def schedule():
    cached_cal = cache.get('cached_cal')
    if cached_cal:
        return cached_cal

    progs = cache.get('programmi_exclude_0')
    if not progs:
        progs = cached_programmi().exclude(status=0)  # see Programmi.models.PROGSTATUS
        cache.set('programmi_exclude_0', progs)
    cal = {"lu": ('Lunedi',     0, []),
           "ma": ('Martedi',    1, []),
           "me": ("Mercoledi",  2, []),
           "gi": ("Giovedi",    3, []),
           "ve": ("Venerdi",    4, []),
           "sa": ("Sabato",     5, []),
           "do": ("Domenica",   6, [])}
    for p in progs:
        cal[p.startgiorno][2].append(p)

    for day in cal.keys():
        cal[day][2].sort(key=lambda x: x.startora)
        # hack per programmi che cominciano a mezzanotte del giorno dopo
        #if len(cal[day][2]) and cal[day][2][0].startora >= time(0, 0) and cal[day][2][0].startora < time(4, 0):
        #    cal[day][2].append(cal[day][2].pop(0))

    orderedcal = cal.values()
    orderedcal.sort(lambda x, y: x[1] - y[1])
    cache.set('cached_cal', orderedcal)
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
    cached_ordered_cal = cache.get('cached_ordered_cal')
    if cached_ordered_cal:
        return cached_ordered_cal

    progs = cache.get('programmi_exclude_0')
    if not progs:
        progs = cached_programmi().exclude(status=0)  # see Programmi.models.PROGSTATUS
        cache.set('programmi_exclude_0', progs)
    if not len(progs):
        return []

    orderedcal = list(progs.values())
    orderedcal.sort(key=lambda x: x["startora"])

    groupedcal = []
    group = [{"startgiorno": x} for x in range(0, 7)]
    tick = orderedcal[0]["startora"]

    for i in orderedcal:
        if i["startora"] != tick:
            group.sort(key=lambda x: x["startgiorno"])
            groupedcal.append(group)
            group = [{"startgiorno": x} for x in range(0, 7)]
            tick = i["startora"]
        if i["startora"] < i["endora"]:
            i['rowspan'] = ((i["endora"].hour * 60 + i["endora"].minute) - (i["startora"].hour * 60 + i["startora"].minute)) / 30
        elif i["startora"] == i["endora"]:
            i['rowspan'] = 48  # 24 hours (sliced in 30 mins cells)
        else:
            i['rowspan'] = ((1440 - (i['startora'].hour * 60 + i['startora'].minute)) +
                            i['endora'].hour * 60 + i['endora'].minute) / 30

        i['url'] = cached_blogs().filter(id=i['blog_id']) and cached_blogs().filter(id=i['blog_id'])[0].url_stripped or ''

        i['startgiorno'] = {'lu': 0,
                            'ma': 1,
                            'me': 2,
                            'gi': 3,
                            've': 4,
                            'sa': 5,
                            'do': 6}[i['startgiorno']]
        i['endgiorno'] = {'lu': 0,
                          'ma': 1,
                          'me': 2,
                          'gi': 3,
                          've': 4,
                          'sa': 5,
                          'do': 6}[i['endgiorno']]
        group[i['startgiorno']] = i

    group.sort(key=lambda x: x["startgiorno"])
    groupedcal.append(group)

    row = 0
    while row < len(groupedcal):
        recheck = False
        for col in range(0, 7):
            i = groupedcal[row][col]
            if 'rowspan' in i and i["rowspan"] > 1:
                j = row + 1
                while j < min(row + i["rowspan"], len(groupedcal)):
                    if "endora" in groupedcal[j][col]:  # COLLISION
                        groupedcal.insert(j, [{"startgiorno": x} for x in range(0, 7)])
                        recheck = True
                        break
                    else:
                        groupedcal[j][col]["busy"] = True
                    j = j + 1
            if recheck:
                break
        if not recheck:
            row = row + 1

    cache.set('cached_ordered_cal', groupedcal)
    return groupedcal


def browse(request, **kwargs):
    blog = kwargs.get('blog', None)
    if not blog:
        blog = cache.get('blog_%s' % request.path)
    if not blog:
        blog = get_object_or_404(Blog, request.path)
    if not blog:
        raise Http404('Not found')
    else:
        cache.set('blog_%s' % request.path, blog)
    page = abs(int(request.GET.get('page', 1)))
    if not blog.blog_generic:
        onair = cached_onair(blog)
    else:
        onair = []
    posts = cached_blog_posts(blog)
    posts = posts.order_by('-published_on')
    paged_posts = Paginator(posts, 6).page(page)
    return render(request, 'blog/post_list.html',
                  {'blog': blog,
                   'browse_posts': True,
                   'recent_posts': paged_posts.object_list,
                   'page_obj': paged_posts,
                   'today_schedule': today_schedule(),
                   'schedule': schedule(),
                   'onair': onair})


def tags(request, tag):
    page = abs(int(request.GET.get('page', 1)))
    tagged_posts = cache.get('posts_tag_%s' % tag)
    if not tagged_posts:
        posts = cached_posts().order_by('-published_on')
        tagged_posts = set([i.tags and tag in i.tags and i for i in posts])
        cache.set('posts_tag_%s' % tag, tagged_posts)

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
                  {'tag': tag,
                   'browse_posts': True,
                   'recent_posts': paged_posts.object_list,
                   'page_obj': paged_posts,
                   'today_schedule': today_schedule(),
                   'schedule': schedule()})


def review(request, review_key):
    post = get_object_or_404(Post, review_key=review_key)
    return show_post(request, post, review=True)


def show_post(request, post, review=False):
    recent_posts = cached_blog_posts(post.blog)
    recent_posts = recent_posts.order_by('-published_on')[:6]
    return render(request, 'blog/post_detail.html',
                  {'post': post,
                   'blog': post.blog,
                   'recent_posts': recent_posts,
                   'review': review,
                   'today_schedule': today_schedule(),
                   'schedule': schedule()})


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
        header = wide_buttons(self._request, post.title, post.get_absolute_url())
        footer = narrow_buttons(self._request, post.title, post.get_absolute_url())
        footer += '<p><a href="%s#disqus_thread">Leave a comment</a></p>' % url
        return header + post.rendered_content + footer

    def item_author_name(self, post):
        return post.author.get_full_name()

    def item_pubdate(self, post):
        return post.published_on

    def items(self, blog):
        query = cached_blog_posts(blog).order_by(
            '-published_on')
        # TODO: add select_related('author') once it's supported
        return query[:100]


@feedburner
def latest_entries_feed(request, *args, **kwargs):
    feed = LatestEntriesFeed()
    feed._request = request
    return feed(request, *args, **kwargs)
