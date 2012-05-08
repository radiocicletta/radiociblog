from .models import Blog, Post
from programmi.models import Programmi
from django.contrib import admin
from minicms.admin import BaseAdmin



class BlogAdmin(BaseAdmin):
    list_display = ('title', 'url','utente')
    search_fields = ('title',)
    ordering = ('url',)


    def queryset(self, request):
        qs = super(BaseAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(utente=request.user.id)

class PostAdmin(BaseAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'blog', 'content', 'published'),
        }),
        #('Advanced options', {
         #   'classes': ('collapse',),
          #  'fields': ('author', 'published_on', 'review_key'),
        #}),
    )
    #exclude = ('author',)
    list_display = ('title', 'author', 'published_on', 'published')
    search_fields = ('url',)
    ordering = ('-last_update',)


    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
    
    def queryset(self, request):
    	if request.user.is_superuser:
		fieldsets = ((None,{'fields':('title','blog','content','published'),}),
		             ('Advanced options',{'classes':('collapse',),'fields':('author','published_on','review_key'),}),)
        	return Post.objects.all()
    	return Post.objects.filter(author=request.user)
#filtro di forza nella dropdown i blog che non competono all'utente
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'blog':
            kwargs['queryset'] = Blog.objects.filter(utente=request.user.id)
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



class ProgrammiAdmin(BaseAdmin):
    list_display = ('title', 'descr')
    search_fields = ('title',)
    ordering = ('title',)

    def queryset(self, request):
        qs = super(BaseAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Programmi, ProgrammiAdmin)
o='''
    def queryset(self, request):
    	if request.user.is_superuser:
        	return Entry.objects.all()
    	return Entry.objects.filter(author=request.user)
	
    def has_change_permission(self, request, obj=None):
	user = request.user
        #has_class_permission = super(EntryAdmin, self).has_change_permission(request, obj)
	#vedo se l'user ha il permesso per il blog relativo al post
        if obj is not None:
		has_class_permission = user.has_perm('blog.'+obj.blog.title)
	else:
		has_class_permission = None
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True
'''
