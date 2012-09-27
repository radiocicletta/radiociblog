from blog.models import Blog, Post
from datetime import datetime
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.utils import simplejson
from models import Programmi
from blog.views import cached_programmi

def progjson(request):
    programmi = cached_programmi()
    events=[]
    next={}
    for p in programmi:
        events.append(p.tojson())
        #n=p.mynext()
        #if n:
        #   next[n[0]]=n[1]   
    return HttpResponse(simplejson.dumps({'programmi':events,'adesso':{"id":0,"start": ["s","now"],"end":["s","now"],"title":"ADESSO"}}), mimetype='application/json')


def modjson(request):
    programmi = cached_programmi()
    events=[]
    next={}
    for p in programmi:
        blog = p.get_blog()
        logo = blog.get_logo()
        events.append({ "Program_id": p.id,
                 "giorno": p.startgiorno,
                 "ora_in": p.startora.hour,
                 "minuti_in": p.startora.minute,
                 "ora_out": p.endora.hour,
                 "minuti_out": p.endora.minute,
                 "stato": p.status,
                 "descrizione": p.descr or blog.description,
                 "blog_id":blog.id,
                 "blog_url":blog.url,
                 "logo":logo and logo.to_json() or '',
                 "nome": p.title})
    return HttpResponse(simplejson.dumps({'programmi':events,'adesso':{"id":0,"start": ["s","now"],"end":["s","now"],"title":"ADESSO"}}), mimetype='application/json')
