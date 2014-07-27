from plogo.models import Plogo
from django.contrib import admin


class PlogoAdmin(admin.ModelAdmin):
    list_display = ('title', 'descr')
    search_fields = ('title',)

admin.site.register(Plogo, PlogoAdmin)
