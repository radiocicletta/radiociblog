from django.db import models
from django.db.models import CharField, \
    TimeField, DateField, BooleanField, ForeignKey, \
    ManyToManyField
from django.core.cache import cache
from plogo.models import Plogo
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

    title = CharField(
        max_length=200,
        help_text='Titolo del programma')
    descr = CharField(
        null=True, blank=True,
        max_length=200,
        help_text='descrizione (opzionale)')
    successivo = BooleanField(
        default=False,
        help_text="Check se l'orario del programma"
        " sconfina al giorno successivo (supera le 23.59)")
    logo = ForeignKey(
        Plogo,
        related_name='program_logo',
        blank=True,
        null=True)
    mixcloud_playlist = CharField(
        'Mixcloud playlist',
        max_length=200,
        blank=True,
        null=True,
        help_text='Optional: Add a mixcloud playlist')
    twitter = CharField(
        'Account twitter',
        max_length=200,
        blank=True,
        null=True,
        help_text='Optional: Add a twitter account')
    facebook_page_or_user = CharField(
        'Pagina o utente facebook',
        max_length=200,
        blank=True,
        null=True,
        help_text='Optional: Add a facebook username/page id')

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
        bloglogo = blog.get_logo()
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
            "logo": self.logo and bloglogo.to_json() or ''}


class Schedule(models.Model):
    list_display = ('name', 'start', 'stop')
    name = CharField(
        max_length=200,
        help_text="Nome del palinsesto",
        blank=False,
        null=False
    )
    start = DateField()
    stop = DateField()
    members = ManyToManyField(
        Programmi,
        through='OnAir',
        related_name="members")

    def __unicode__(self):
        return self.name


class OnAir(models.Model):
    schedule = ForeignKey(Schedule, related_name='onair')
    programmi = ForeignKey(Programmi, related_name='onair')
    start_day = CharField(
        max_length=2,
        choices=GIORNI,
        help_text='Scegliere il giorno oppure'
        ' SINGOLO se si ripete solo una volta')
    start_hour = TimeField(
        help_text='ora di inizio (nel formato hh:mm:ss con hh da 00 a 23)')
    end_day = CharField(max_length=2, choices=GIORNI)
    end_hour = TimeField()
