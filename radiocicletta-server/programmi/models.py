from django.db import models
from django.core.cache import cache
#from pytz.gae import pytz
import pytz

tzdata = pytz.timezone('Europe/Rome')

PROGSTATUS = (
    ('0', 'ferie (offair)'),
    ('1', 'in programmazione'),
    ('2', 'special'),
    ('3', 'cambiato'),
    ('4', 'nuovo'),
    ('5', 'replica'))
PRIMA = {
    'lu': 'do',
    'ma': 'lu',
    'me': 'ma',
    'gi': 'me',
    've': 'gi',
    'sa': 've',
    'do': 'lu',
    's': 's'}
GIORNI = (('lu', 'LUNEDI'),
          ('ma', 'MARTEDI'),
          ('me', 'MERCOLEDI'),
          ('gi', 'GIOVEDI'),
          ('ve', 'VENERDI'),
          ('sa', 'SABATO'),
          ('do', 'DOMENICA'),
          ('s', 'SINGOLO'))


class Programmi(models.Model):
    verbose_name = "programmi"
    list_display = ('title', 'start_day', 'start_hour')

    title = models.CharField(max_length=200, help_text='Titolo del programma')
    descr = models.CharField(
        null=True, blank=True,
        max_length=200,
        help_text='descrizione (opzionale)')
    status = models.CharField(
        max_length=1,
        choices=PROGSTATUS)
    start_day = models.CharField(
        max_length=2,
        choices=GIORNI,
        help_text='Scegliere il giorno oppure'
        ' SINGOLO se si ripete solo una volta')
    start_hour = models.TimeField(
        help_text='ora di inizio (nel formato hh:mm:ss con hh da 00 a 23)')
    end_day = models.CharField(max_length=2, choices=GIORNI)
    end_hour = models.TimeField()
    successivo = models.BooleanField(
        default=False,
        help_text="Check se l'orario del programma"
        " sconfina al giorno successivo (supera le 23.59)")

    def __unicode__(self):
        return self.title
    # preparo il json e scalo il giorno se il programma scavalla la mezzanotte
    # (il js che renderizza se n'ha a male altrimenti)

    def get_blog(self):
        cached_blog = cache.get('programma_%s_blog' % self.pk)
        if not cached_blog:
            cache.set('programma_%s_blog' % self.pk, self.blog)
            return self.blog
        return cached_blog

    def tojson(self):
        blog = self.get_blog()
        logo = blog.get_logo()
        return {
            "id": self.id,
            "title": self.title,
            "start": [self.start_day,
                      self.start_hour.hour,
                      self.start_hour.minute],
            "end": [self.end_day
                    if not self.successivo
                    else PRIMA[self.end_day],
                    self.end_hour.hour,
                    self.end_hour.minute],
            "stato": self.status,
            "blog_id": blog.id,
            "blog_url": blog.url,
            "logo": logo and logo.to_json() or ''}
