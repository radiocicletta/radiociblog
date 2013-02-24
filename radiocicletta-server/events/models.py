from django.db import models


def cached_posterevents():
    b = cache.get('posterevents')
    if not b:
        b = PosterEvent.objects.all()
        cache.add('posterevents', b)
    return b


class PosterEvent(models.Model):
    url =  models.URLField('Link evento', verify_exists=False, blank=False, help_text='')
    image_url = models.URLField('Immagine correlata', verify_exists=False, blank=False)
    title = models.CharField(max_length=200)
    published_on = models.DateTimeField(null=True, blank=True, help_text='Optional (filled automatically when publishing)')
    published_until = models.DateTimeField(null=True, blank=False)

    def __unicode__(self):
        return self.title
 
