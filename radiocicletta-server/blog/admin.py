from .models import Blog, Post, User
from programmi.models import Programmi
from plogo.models import Plogo
from django.contrib import admin
from minicms.admin import BaseAdmin
from django import forms
from django.core.cache import cache
import logging


logger=logging.getLogger(__name__)


class BlogForm(forms.ModelForm):

    # many thanks to https://github.com/tingletech/collengine/blob/master/items/admin.py
    utenti = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Blog

    def save(self, commit=True):
        model = super(BlogForm, self).save(commit=False)
        model.utenti = [utenti.id for utenti in model.utenti]
        if commit:
            model.save()
        return model


class BlogAdmin(BaseAdmin):
    list_display = ('title', 'url', 'related_utenti')
    search_fields = ('title',)
    ordering = ('title', 'url')
    form = BlogForm

#    def queryset(self, request):
#        if not request.user.is_superuser:
#            filt = [b.id for b in filter( lambda x: request.user.id in x.utenti, Blog.objects.all())]
#            blogs = Blog.objects.all()
#            i = 0
#            logger.warning(blogs)
#            logger.warning(blogs._result_cache)
#            while i < len(blogs._result_cache):
#                if blogs._result_cache[i].id in filt:
#                    blogs._result_cache.pop(i)
#                else:
#                    i = i + 1
#            return blogs
#        qs = super(BaseAdmin, self).queryset(request)
#        return qs


class PostAdmin(BaseAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'blog', 'content', 'published', 'tags'),
        }),
        #('Advanced options', {
        #    'classes': ('collapse',),
        #    'fields': ('author', 'published_on', 'review_key'),
        #}),
    )
    #exclude = ('author',)
    list_display = ('title', 'in_blog', 'author', 'published_on', 'published')
    search_fields = ('title', 'url', 'author')
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
        if db_field.name == 'blog' and request.method == 'GET':
            qs_blog_user = Blog.objects.all()

            kwargs['queryset'] = qs_blog_user
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ProgrammiAdmin(BaseAdmin):
    list_display = ('title', 'descr', 'startgiorno', 'startora')
    search_fields = ()  # ('title',)
    ordering = ('title',)

#    def queryset(self, request):
#        qs = super(BaseAdmin, self).queryset(request)
#        if request.user.is_superuser:
#            return qs
#        return qs.filter(author=request.user)


class PlogoAdmin(admin.ModelAdmin):
    list_display = ('title', 'descr')
    search_fields = ('title',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Programmi, ProgrammiAdmin)
admin.site.register(Plogo, PlogoAdmin)
