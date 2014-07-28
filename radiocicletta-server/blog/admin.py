from .models import Blog, Post
from programmi.models import Programmi
from django.contrib import admin
from minicms.admin import BaseAdmin
import logging


logger=logging.getLogger(__name__)

class BlogAdmin(BaseAdmin):
    list_display = ('title', 'url', 'related_utenti')
    search_fields = ('title',)
    ordering = ('title', 'url')
    def queryset(self, request):
        if request.user.is_superuser:
            qs = super(BaseAdmin, self).queryset(request)
            return qs
        return Blog.objects.filter(
            utenti__in=[request.user.id])



class PostAdmin(BaseAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'blog', 'content', 'published', 'tags'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('author', 'published_on', 'review_key'),
        }),
    )
    #exclude = ('author',)
    list_display = ('title', 'in_blog', 'author', 'published_on', 'published', 'url')
    search_fields = ('title', )
    ordering = ('-last_update',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def queryset(self, request):
        if request.user.is_superuser:
            fieldsets = ((None,
                          {'fields':
                           ('title',
                            'blog',
                            'content',
                            'published',
                            'tags')}),
                        ('Advanced options',
                         {'classes':
                          ('collapse',),
                          'fields':
                          ('author', 'published_on',
                           'review_key')}))
            return Post.objects.all()
        return Post.objects.filter(author=request.user)

    #filtro di forza nella dropdown i blog che non competono all'utente
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'blog' and request.method == 'GET' and \
                not request.user.is_superuser:
            qs_blog_user = Blog.objects.filter(
                utenti__in=[request.user.id])

            kwargs['queryset'] = qs_blog_user
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ProgrammiAdmin(BaseAdmin):
    list_display = ('title', 'descr', 'start_day', 'start_hour')
    search_fields = ()  # ('title',)
    ordering = ('title',)

    def queryset(self, request):
        qs = super(BaseAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Programmi, ProgrammiAdmin)
