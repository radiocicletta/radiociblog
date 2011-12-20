from blog.models import Blog, Post
from datetime import datetime
from django.conf import settings
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.utils.feedgenerator import Atom1Feed
from django.views.generic import ListView
from simplesocial.api import wide_buttons, narrow_buttons
from amministra.utils import get_datatables_records
from django.template import loader, Context
from django.http import HttpResponse
from django.contrib.auth.models import User

def posttableline(post):
	return 	'["%s%s","%s","%s"]'%(post.id,post.title,post.published_on,post.published)

@login_required 
def index(request):
    return render(request, 'index.html', {'posturl': '/amministra/postlist', 'root_path':'/amministra/','logout_url ':'/amministra/' })


def poststable(request):
    #recent_posts = Post.objects.filter(author=request.user.id,published=True)
    posts = Post.objects.filter(author=request.user.id)
    #columnIndexNameMap is required for correct sorting behavior
    columnIndexNameMap = { 0: 'id', 1 : 'title', 2: 'data', 3: 'pub'}
    #path to template used to generate json (optional)
    jsonTemplatePath = 'json_post.txt'
    #call to generic function from utils
    return get_datatables_records(request,posts, columnIndexNameMap, jsonTemplatePath)

def test(request):
	 return render(request, 'test.html', {'test': "" })

