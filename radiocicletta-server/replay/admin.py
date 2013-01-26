from django.contrib import admin
from django.shortcuts import  render
from replay.models import Replay
from django.conf.urls.defaults import *
from django import forms
from django.contrib.admin import widgets
import logging
from models import Replay
import datetime

logger = logging.getLogger(__name__)


class ReplayForm(forms.ModelForm):

    replicafile = forms.FileField(label = "File da caricare", required = False, show_hidden_initial = True)
    date = forms.DateTimeField(label = "Data e ora della riproduzione", required = True)
    description = forms.CharField(label = "Descrizione", required = False )
    #dropboxpath = forms.Field(input=None)
    date_hierarchy = 'pub_date'
    action_form = None

    class Meta:
        model = Replay

    def __init__(self, *args, **kwargs):
        super(ReplayForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = widgets.AdminSplitDateTime()


class ReplayAdmin(admin.ModelAdmin):
    fields = ()
    list_display = ('description', 'date')
    odering = ('date')
    form = ReplayForm

    def get_urls(self):
        urls = super(ReplayAdmin, self).get_urls()
        return patterns('',
                        (r'^purgeold/$', self.admin_site.admin_view(self.purgeold))
               ) + urls

    def purgeold(self, request):
        objects = Replay.objects.filter(date__lt=datetime.datetime.now())
        if not request.user.has_perms('Replay.can_edit'):
            perms_lacking = objects
            deleted_objects = objects
        else:
            perms_lacking = []
            deleted_objects = []
            for obj in objects:
                deleted_objects.append(obj.description)
                obj.delete()

        return render(request, 'admin/replay/purge.html',
                {'deleted_objects': deleted_objects,
                 'perms_lacking':   perms_lacking,
                 'objects_name':    'Replay'})

    def save_model(self, request, obj, form, change):
        frm = form.cleaned_data
        obj.date = frm['date']
        obj.description = u''.join([frm['description'], ' (Replay - ', frm['date'].isoformat(), ')'])
        obj.save()


    def get_readonly_fields(self, request, obj=None):
        return obj and ['description', 'date'] or []


admin.site.register(Replay, ReplayAdmin)
