"""
Models for object-level permissions
"""

from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

from djangotoolbox.fields import SetField


class PermissionType(models.Model):
    content_type = models.CharField(max_length=256)
    permission_name = models.CharField(max_length=64, null=True)

    def __unicode__(self):
        return u'%s:%s' % (self.content_type, self.permission_name)


class BaseObjectPermission(models.Model):
    permission_set = SetField(models.CharField(max_length=64))

    content_type = models.CharField(max_length=256)
    object_id = models.PositiveIntegerField()

    def get_permissions(self):
        return self.permission_set

    def set_permissions(self, permission_list):
        self.permission_set = permission_list
    
    permissions = property(get_permissions, set_permissions)

    class Meta:
        abstract = True


class ObjectPermission(BaseObjectPermission):
    user_id = models.CharField(max_length=32, null=True)
    
    def __unicode__(self):
        return u'%s:%s:%i'%(self.user_id, self.content_type, self.object_id)


class GroupObjectPermission(BaseObjectPermission):
    group_id = models.CharField(max_length=32, null=True)

    def __unicode__(self):
        return u'%s:%s:%i'%(self.group_id, self.content_type, self.object_id)
