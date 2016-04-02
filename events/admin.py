from django.contrib import admin
from minicms.admin import BaseAdmin
from events.models import PosterEvent

class PosterEventAdmin(BaseAdmin):
    list_display = ('title', 'url')
    search_fields = ('title',)
    ordering = ('title',)

admin.site.register(PosterEvent, PosterEventAdmin)
