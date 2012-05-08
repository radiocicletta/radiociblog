from django.contrib.auth.models import User, Group
from django.db import models
from django.contrib.contenttypes.models import ContentType

from .models import ObjectPermission, PermissionType, GroupObjectPermission


def check_registered_permissions_for_obj(permissions, obj, is_ct=False):
    if is_ct:
        ct = obj
    else:
        ct = get_content_type_string(obj)    
    registered_permission_list = list(PermissionType.objects.filter(content_type=
                                                                    ct).values_list('permission_name', flat=True))
    checked_permissions = set()
    for perm in permissions:
        try:
            checked_permissions.add(registered_permission_list.pop(registered_permission_list.index(perm)))
        except ValueError:
            return []

    return checked_permissions

#def set_user_permissions(user, permission_list)

def get_group_id_list(user_id):
    from permission_backend_nonrel.models import UserPermissionList

    try:
        return UserPermissionList.objects.get(user__id=user_id).group_fk_list
    except UserPermissionList.DoesNotExist:
        return []

def get_content_type_string(obj):
        return (obj._meta.app_label + '.' + obj.__class__.__name__).lower()


def register_obj_permission(model_class, perm):
    """
    creates a PermissionType object with permission perm for the model model_class
    """

    ct = get_content_type_string(model_class())
    pt = PermissionType.objects.filter(content_type=ct,
                                       permission_name=perm)

    if pt.count() != 0:
        return False # already registered
    else:
        pt = PermissionType(content_type=ct, permission_name=perm)
        pt.save()
        return True

def _add_obj_permissions(cls, filt, obj, user, new_permissions):
    ct = get_content_type_string(obj)
    try:
        perm_obj = cls.objects.get(content_type=ct,
                                   object_id=obj.pk, **filt)
    except cls.DoesNotExist:
        perm_obj = cls(content_type=ct,
                       object_id=obj.pk, **filt)

    permissions = perm_obj.permissions or set()

    new_permissions = check_registered_permissions_for_obj(new_permissions, obj)
    
    if new_permissions == []:
        return False
    
    permissions.update(new_permissions)        
    
    perm_obj.permissions =  permissions
    perm_obj.save()
    return True

def add_obj_permissions_to_user(obj, new_permissions, user):
    """
    add permission_list for user to model

    returns False if permission_list contains unregistered permissions
    or model is no instance of models.Model or user is no instance of
    django.contrib.auth.models.User

    returns True if permission_list is saved
    """
    
    if isinstance(user, User) and isinstance(obj, models.Model):    
        filt = {'user_id': user.pk,}

        return _add_obj_permissions(ObjectPermission, filt, obj, user, new_permissions)
    else:
        return False

def add_obj_permissions_to_group(obj, new_permissions, group):
    if isinstance(group, Group) and isinstance(obj, models.Model):    
        filt = {'group_id': group.pk,}

        return _add_obj_permissions(GroupObjectPermission, filt, obj, group, new_permissions)
    else:
        return False    

def add_user_to_group(user, group):
    from permission_backend_nonrel.utils import add_user_to_group as _add_user_to_group
    _add_user_to_group(user, group)
