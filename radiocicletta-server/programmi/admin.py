from programmi.models import Programmi
from django.contrib import admin


class ProgrammiAdmin(admin.ModelAdmin):
    list_display = ('title', 'descr', 'start_day', 'start_hour')
    search_fields = ()  # ('title',)
    ordering = ('title',)

    def queryset(self, request):
        qs = super(admin.ModelAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

admin.site.register(Programmi, ProgrammiAdmin)

