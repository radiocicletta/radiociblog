from django.http import HttpResponse
import json
from blog.views import cached_programmi


def progjson(request):
    programmi = cached_programmi()
    events = []
    for p in programmi:
        events.append(p.tojson())
    return HttpResponse(json.dumps({'programmi': events,
                                    'adesso': {"id": 0,
                                               "start": ["s", "now"],
                                               "end": ["s", "now"],
                                               "title": "ADESSO"}
                                    }),
                        mimetype='application/json')


def modjson(request):
    programmi = cached_programmi()
    events = []
    for p in programmi:
        blog = p.get_blog()
        logo = blog.get_logo()
        events.append({"Program_id": p.id,
                       "giorno": p.start_day,
                       "ora_in": p.start_hour.hour,
                       "minuti_in": p.start_hour.minute,
                       "ora_out": p.end_hour.hour,
                       "minuti_out": p.end_hour.minute,
                       "stato": p.status,
                       "descrizione": p.descr or blog.description,
                       "blog_id": blog.id,
                       "blog_url": blog.url,
                       "logo": logo and logo.to_json() or '',
                       "nome": p.title})
    return HttpResponse(simplejson.dumps({'programmi': events,
                                          'adesso': {"id": 0,
                                                     "start": ["s", "now"],
                                                     "end": ["s", "now"],
                                                     "title": "ADESSO"}
                                          }),
                        mimetype='application/json')
