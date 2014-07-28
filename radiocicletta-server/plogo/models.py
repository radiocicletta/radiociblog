from django.db import models


class Plogo(models.Model):
    verbose_name = "logo"
    title = models.CharField(
        max_length=200,
        help_text='Titolo del logo')
    descr = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        help_text='descrizione per l\'alt (opzionale)')
    url = models.CharField(
        'URL',
        max_length=200,
        help_text='Effettua l\'upload con il campo in cima alla pagina. <br>'
        'Se tutto e\' andato bene dovrebbe riempirsi da solo. ')

    class Meta:
        verbose_name_plural = "loghi"

    def __unicode__(self):
        return self.title

    def to_json(self):
        return {
            'title': self.title,
            'descr': self.descr,
            'url': self.url
        }
