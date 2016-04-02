from programmi.models import Programmi, Schedule, OnAir
from django.contrib import admin


class ProgrammiAdmin(admin.ModelAdmin):
    list_display = ('title', 'descr')
    search_fields = ()  # ('title',)
    ordering = ('title',)

    def queryset(self, request):
        qs = super(admin.ModelAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name','start','stop')
    ordering = ('name','start','stop')

class OnAirAdmin(admin.ModelAdmin):
    list_display = ('programmi', 'schedule','start_day','start_hour')
    ordering = ('schedule','start_day','start_hour')

admin.site.register(Programmi, ProgrammiAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(OnAir, OnAirAdmin)

