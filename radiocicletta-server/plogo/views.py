from blog.models import Blog, Post
from datetime import datetime
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.utils import simplejson
from models import BLogo




