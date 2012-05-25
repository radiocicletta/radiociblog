from .models import Blog, Post
from datetime import datetime, time
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.utils.feedgenerator import Atom1Feed
from django.views.generic import ListView
from simplesocial.api import wide_buttons, narrow_buttons
from programmi.models import Programmi
import logging
logger = logging.getLogger(__name__)

### pagine "statiche"
def oldhome(request):
    blogs = Blog.objects.all()
    recent_posts = Post.objects.filter(published=True)
    recent_posts = recent_posts.order_by('-published_on')[:6]
    return render(request, 'blog/index.html', {'blogs':blogs, 'recent_posts': recent_posts, 'schedule':schedule()})
def foto(request):
    return render(request, 'blog/foto.html', {'schedule':schedule()})
def programmi(request):
    programmi = Programmi.objects.all()
    return render(request, 'blog/programmi.html', {'programmi': programmi, 'schedule':schedule()})
def chi(request):
    return render(request, 'blog/chi.html', {'schedule':schedule()})
def aiuta(request):
    return render(request, 'blog/aiuta.html', {'schedule':schedule()})
def down(request):
    return render(request, 'blog/download.html', {'schedule':schedule()})

### pagine bloggose
def tuttib(request):
    blogs = Blog.objects.all()
    recent_posts = Post.objects.filter(published=True)
    recent_posts = recent_posts.order_by('-published_on')[:6]
    return render(request, 'blog/blog.html', {'blogs':blogs, 'recent_posts': recent_posts, 'schedule':schedule()})


def schedule():
    progs = Programmi.objects.all().exclude(status = 0) # see Programmi.models.PROGSTATUS
    cal = {"lu":('Lunedi',      0, []),
            "ma":('Martedi',     1, []),
            "me":("Mercoledi",  2, []),
            "gi":("Giovedi",    3, []),
            "ve":("Venerdi",    4, []),
            "sa":("Sabato",     5, []),
            "do":("Domenica",   6, []) }
    for p in progs:
        cal[p.startgiorno][2].append(p)

    for day in cal.keys():
        cal[day][2].sort(key=lambda x: x.startora)
        if len(cal[day][2]) and cal[day][2][0].startora == time(0, 0): # hack per programmi che cominciano a mezzanotte del giorno dopo
            cal[day][2].append(cal[day][2].pop(0))

    orderedcal = cal.values()
    orderedcal.sort(lambda x,y: x[1] - y[1])
    return orderedcal

def blog_browse(request, url):
    blog = get_object_or_404(Blog, url='/' + url)
    recent_posts = Post.objects.filter(blog=blog, published=True)
    recent_posts = recent_posts.order_by('-published_on')[:6]
    return render(request, 'blog/post_list.html',
        {'blog': blog, 'recent_posts': recent_posts, 'schedule':schedule()})


def review(request, review_key):
    logger.warn(review_key)
    post = get_object_or_404(Post, review_key=review_key)
    return show_post(request, post, review=True)

def show_post(request, post, review=False):
    recent_posts = Post.objects.filter(blog=post.blog, published=True)
    recent_posts = recent_posts.order_by('-published_on')[:6]
    return render(request, 'blog/post_detail.html',
        {'post': post, 'blog': post.blog, 'recent_posts': recent_posts, 'review': review, 'schedule':schedule()})

class BrowseView(ListView):
    paginate_by = 8

    def dispatch(self, request, blog):
        if request.GET.get('page') == '1':
            return HttpResponseRedirect(request.path)
        return super(BrowseView, self).dispatch(request, blog=blog)

    def get_queryset(self):
        query = Post.objects.filter(blog=self.kwargs['blog'], published=True)
        # TODO: add select_related('author')
        return query.order_by('-published_on')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BrowseView, self).get_context_data(**kwargs)
        context.update({'blog': self.kwargs['blog'],
                        'schedule': schedule(),
                        'recent_posts': self.get_queryset()[:6],
                        'browse_posts': True})
        return context

browse = BrowseView.as_view()

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
        query = Post.objects.filter(blog=blog, published=True).order_by(
            '-published_on')
        # TODO: add select_related('author') once it's supported
        return query[:100]

@feedburner
def latest_entries_feed(request, *args, **kwargs):
    feed = LatestEntriesFeed()
    feed._request = request
    return feed(request, *args, **kwargs)
