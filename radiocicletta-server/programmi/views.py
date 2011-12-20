from blog.models import Blog, Post
from datetime import datetime
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.utils import simplejson
from models import Programmi

def progjson(request):
    programmi = Programmi.objects.all()
    events=[{"id":0,"start": ["s","now"],"end":["s","now"],"title":"ADESSO"}]
    next={}
    for p in programmi:
        events.append(p.tojson())
        n=p.mynext()
        if n:
           next[n[0]]=n[1]   
    return HttpResponse(simplejson.dumps({'events':events,'next':next}), mimetype='text/plain')

