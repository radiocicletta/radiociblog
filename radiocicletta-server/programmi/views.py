from django.http import HttpResponse
import json
from .models import Programmi
from config.models import SiteConfiguration

config = SiteConfiguration.get_solo()


def progjson(request):
    programmi = config.active_schedule.onair
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
    programmi = config.active_schedule.onair
    events = []
    for p in programmi:
        blog = p.programmi.blog
        events.append({"Program_id": p.id,
                       "giorno": p.start_day,
                       "ora_in": p.start_hour.hour,
                       "minuti_in": p.start_hour.minute,
                       "ora_out": p.end_hour.hour,
                       "minuti_out": p.end_hour.minute,
                       "descrizione": p.programmi.descr,
                       "blog_id": blog and blog.id,
                       "blog_url": p.url,
                       "logo": p.programmi.logo.url,
                       "nome": p.programmi.title})
    return HttpResponse(json.dumps({'programmi': events,
                                     'adesso': {"id": 0,
                                                "start": ["s", "now"],
                                                "end": ["s", "now"],
                                                "title": "ADESSO"}
                                     }),
                        mimetype='application/json')
