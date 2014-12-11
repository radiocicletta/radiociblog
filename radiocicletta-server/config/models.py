from django.db import models

from solo.models import SingletonModel
from programmi.models import Schedule


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name')
    maintenance_mode = models.BooleanField(default=False)
    active_schedule = models.ForeignKey(
        Schedule,
        related_name='schedule',
        default=None,
        blank=True,
        null=True)

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
