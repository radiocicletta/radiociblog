from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
import logging

logger=logging.getLogger(__name__)


class AutoSlug(widgets.TextInput):

    media =  forms.Media(
            js=('slug.js' ,)
        )

    def __init__(self, *args, **kwargs):
        self.data_source = kwargs.pop('data_source', None)

        attrs = {
            'class': 'autoslug',
            'data-source': self.data_source
        }
        super(AutoSlug, self).__init__(attrs)

