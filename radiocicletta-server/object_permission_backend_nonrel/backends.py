from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from .models import ObjectPermission, GroupObjectPermission
from .utils import get_content_type_string, get_group_id_list
import logging


PERM_STRING_TEMPLATE = '%s.%s.%s'

class ObjectPermBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = True
    
    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, obj=None):

        if not user_obj.is_authenticated():
            user_id = settings.ANONYMOUS_USER_ID
        else:
            user_id = user_obj.pk
        if obj:
            perm_str = PERM_STRING_TEMPLATE % (get_content_type_string(obj), obj.pk, perm) 
        else:
            perm_str = ''

        if hasattr(user_obj, '_perm_cache'):
            if perm_str in user_obj._perm_cache:
                return True
        else:
            setattr(user_obj, '_perm_cache', set())

        new_perms = set()
        if obj:
            ct = get_content_type_string(obj)
            new_perms.update(self._get_user_permission(user_id, obj.pk, ct))
            new_perms.update(self._get_group_permission(user_id, obj.pk, ct))

            user_obj._perm_cache.update(new_perms)
        return perm_str in new_perms
    
    def get_all_permissions(self, user_obj, obj=None):
        return None
    
    def get_group_permissions(self, user_obj, obj=None):
        return None

    def _create_permission_strings(self, permission_objs):
        new_perms = []
        for p in permission_objs:
                for perm in p.permissions:
                    new_perms.append(PERM_STRING_TEMPLATE % (p.content_type, p.object_id, perm))
        return new_perms

    def _get_user_permission(self, user_id, object_id, ct):
        current_permission_objs = ObjectPermission.objects.filter(user_id=user_id, content_type=ct, object_id=object_id)
        return self._create_permission_strings(current_permission_objs)

    def _get_group_permission(self, user_id, object_id, ct):
        group_id_list =  get_group_id_list(user_id)
        current_permission_objs = GroupObjectPermission.objects.filter(group_id__in=group_id_list, content_type=ct, object_id=object_id)
        return self._create_permission_strings(current_permission_objs)
