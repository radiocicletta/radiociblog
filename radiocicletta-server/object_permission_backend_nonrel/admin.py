import settings
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from .utils import check_registered_permissions_for_obj, get_content_type_string
from .models import PermissionType, ObjectPermission, GroupObjectPermission


def create_user_permission_obj(modeladmin, request, queryset):
    for obj in queryset:
         ct = get_content_type_string(obj)
         perm_obj = ObjectPermission.objects.create(content_type=ct,
                                                    object_id=obj.pk)

def create_group_permission_obj(modeladmin, request, queryset):
    for obj in queryset:
         ct = get_content_type_string.objects.get_for_model(obj)
         perm_obj = GroupObjectPermission.objects.create(content_type=ct,
                                                         object_id=obj.pk)

admin.site.add_action(create_user_permission_obj, 'Create Object Permission for a user')
admin.site.add_action(create_group_permission_obj, 'Create Object Permission for a group')


class BaseObjectPermissionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseObjectPermissionForm, self).__init__(*args, **kwargs)

        self.fields['obj_permission_list'] = forms.MultipleChoiceField(required=False)

        try:
            permission_types = PermissionType.objects.filter(content_type=kwargs['instance'].content_type)
        except KeyError:
            permission_types = []
            
        choices = []
        cls_list = set()
        for pt in permission_types:
            choices.append([pt.permission_name,  '%s:%s' %( pt.content_type, pt.permission_name)])
           
        self.fields['obj_permission_list'].choices = choices

        try:
            selected = self.Meta.model.objects.get(id=kwargs['instance'].pk)
            initial = []
            for permission in kwargs['instance'].permissions:
                initial.append(permission)
        
                self.fields['obj_permission_list'].initial = initial
        except KeyError:
            pass

class ObjectPermissionForm(BaseObjectPermissionForm):
    obj_permission_list = forms.MultipleChoiceField(required=False)
    user = forms.ChoiceField(required=True)

    def __init__(self, *args, **kwargs):
        super(ObjectPermissionForm, self).__init__(*args, **kwargs)        
        users = User.objects.all()
        choices = [[user.pk, user.username] for user in users]
        self.fields['user'].choices = choices
        try:
            self.fields['user'].initial = kwargs['instance'].user_id
        except KeyError:
            pass

    class Meta:
        model = ObjectPermission
        exclude = ('permission_set', 'user_id')


class BaseObjectPermissionAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.permissions = check_registered_permissions_for_obj(form.cleaned_data['obj_permission_list'], obj.content_type, is_ct=True)
        super(BaseObjectPermissionAdmin, self).save_model(request, obj, form, change)


class ObjectPermissionAdmin(BaseObjectPermissionAdmin):
    form = ObjectPermissionForm

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.user_id = form.cleaned_data['user']
        super(ObjectPermissionAdmin, self).save_model(request, obj, form, change)

        
class GroupObjectPermissionForm(BaseObjectPermissionForm):
     obj_permission_list = forms.MultipleChoiceField(required=False)
     group = forms.ChoiceField(required=True)

     def __init__(self, *args, **kwargs):
        super(GroupObjectPermissionForm, self).__init__(*args, **kwargs)        
        groups = Group.objects.all()
        choices = [[group.pk, group.name] for group in groups]
        self.fields['group'].choices = choices
        try:
            self.fields['group'].initial = kwargs['instance'].group_id
        except KeyError:
            pass
        
     class Meta:
         model = GroupObjectPermission
         exclude = ('permission_set', 'group_id')


class GroupObjectPermissionAdmin(BaseObjectPermissionAdmin):
    form = GroupObjectPermissionForm

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.group_id = form.cleaned_data['group']
        super(GroupObjectPermissionAdmin, self).save_model(request, obj, form, change)


class PermissionTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermissionTypeForm, self).__init__(*args, **kwargs)

        self.fields['content_type'] = forms.ChoiceField(required=True)
        contenttypes = ContentType.objects.all()

        #choices = [[ct.id, ct] for ct in contenttypes]
        
        choices = []
        initial = None
        for ct in contenttypes:
            choices.append([ct.pk, ct])
            try:
                if kwargs['instance'].content_type == '%s.%s'%(ct.app_label, ct.model):
                    initial = ct.pk
            except KeyError:
                pass
        self.fields['content_type'].choices = choices    
        self.fields['content_type'].initial = initial


        
class PermissionTypeAdmin(admin.ModelAdmin):
    form = PermissionTypeForm

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            try:
                content_type = ContentType.objects.get(id=form.cleaned_data['content_type'])
                obj.content_type = '%s.%s'%(content_type.app_label, content_type.model)
            except ContentType.DoesNotExist:
                pass # raise form error
            
        super(PermissionTypeAdmin, self).save_model(request, obj, form, change)

        
admin.site.register(ObjectPermission, ObjectPermissionAdmin)
admin.site.register(GroupObjectPermission, GroupObjectPermissionAdmin)
admin.site.register(PermissionType, PermissionTypeAdmin)

























