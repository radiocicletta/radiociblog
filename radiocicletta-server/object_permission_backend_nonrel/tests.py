from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

from .utils import add_user_to_group
from permission_backend_nonrel.models import UserPermissionList

from .models import ObjectPermission,PermissionType, GroupObjectPermission
from .utils import add_obj_permissions_to_user, register_obj_permission, add_obj_permissions_to_group, get_content_type_string

class TestObjFoo(models.Model):
    pass

class TestObjBar(models.Model):
    pass

class ObjPermBackendTests(TestCase):
    """
    Tests for the object permission app
    """

    def setUp(self):
        self.user1 = User.objects.create_user('test1', 'test1@test.com', 'test')
        self.user2 = User.objects.create_user('test2', 'test2@test.com', 'test')

        self.obj_foo = TestObjFoo()
        self.obj_foo.id = 1 # add id manually to avoid problem with app engine
        self.obj_foo.save()

        self.obj_bar = TestObjBar()
        self.obj_bar.id = 2 # add id manually to avoid problem with app engine
        self.obj_bar.save()

    def test_permission_creation(self):
               # add permission types for class TestObjFoo
        ct = get_content_type_string(self.obj_foo)        
        pt = PermissionType(content_type=ct, permission_name='view')
        pt.save()
        pt = PermissionType(content_type=ct, permission_name='change')
        pt.save()
        pt = PermissionType(content_type=ct, permission_name='delete')
        pt.save()

        # add permission types for class TestObjBar
        ct_bar = get_content_type_string(self.obj_bar)        
        pt = PermissionType(content_type=ct_bar, permission_name='view')
        pt.save()
        pt = PermissionType(content_type=ct_bar, permission_name='change')
        pt.save()
        pt = PermissionType(content_type=ct_bar, permission_name='delete')
        pt.save()
        
        # create permission object for user1 and obj_foo
        perm_obj = ObjectPermission.objects.create(user_id=self.user1.id,
                                                   content_type=ct, object_id=self.obj_foo.id)

        permission_list = perm_obj.permissions
        permission_list.add('view')
        permission_list.add('change')
        permission_list.add('delete')
        perm_obj.permissions = permission_list
        perm_obj.save()

        self.assertEquals(permission_list, perm_obj.permissions)
        self.assertEquals(self.user1.has_perm('view', self.obj_foo), True)
        self.assertEquals(self.user1.has_perm('change', self.obj_foo), True)
        self.assertEquals(self.user1.has_perm('delete', self.obj_foo), True)

        # create permission object for user1 and obj_bar
        perm_obj = ObjectPermission.objects.create(user_id=self.user1.id,
                                                   content_type=ct_bar, object_id=self.obj_bar.id)
        permission_list = perm_obj.permissions
        permission_list.add('view')
        perm_obj.permissions = permission_list
        perm_obj.save()

        # create permission object for user2 and obj_bar
        perm_obj = ObjectPermission.objects.create(user_id=self.user2.id,
                                                   content_type=ct_bar, object_id=self.obj_bar.id)
        permission_list = perm_obj.permissions
        permission_list.add('view')
        perm_obj.permissions = permission_list
        perm_obj.save()

        # 3 ObjectPermission object has to be created
        self.assertEquals(ObjectPermission.objects.count(), 3)

        # check if user1 has view, change and delete permission for obj_foo
        # and view for obj_bar
        self.assertEquals(self.user1.has_perm('view', self.obj_bar), True)
        self.assertEquals(self.user1.has_perm('change', self.obj_bar), False)
        self.assertEquals(self.user1.has_perm('delete', self.obj_bar), False)

        # user2 doesn't have any permissions for obj_foo and view for obj_bar
        self.assertEquals(self.user2.has_perm('view', self.obj_foo), False)
        self.assertEquals(self.user2.has_perm('change', self.obj_foo), False)
        self.assertEquals(self.user2.has_perm('delete', self.obj_foo), False)

        self.assertEquals(self.user2.has_perm('view', self.obj_bar), True)
        self.assertEquals(self.user2.has_perm('change', self.obj_bar), False)
        self.assertEquals(self.user2.has_perm('delete', self.obj_bar), False)

        
    def test_register_obj_permission_permission(self):
        self.assertEquals(add_obj_permissions_to_user(self.obj_foo, ['view'], self.user1), False)
        self.assertEquals(ObjectPermission.objects.count(), 0)
        self.assertEquals(PermissionType.objects.count(), 0)
        
        register_obj_permission(TestObjFoo, 'view')
        self.assertEquals(PermissionType.objects.count(), 1)
        
        # create permissions with the add_permissions function
        self.assertEquals(add_obj_permissions_to_user(self.obj_foo, ['view', 'change'], self.user1), False)
        
        self.user1 = User.objects.get(id=self.user1.id)
        self.assertEquals(ObjectPermission.objects.count(), 0)
        self.assertEquals(self.user1.has_perm('view', self.obj_foo), False)
        self.assertEquals(self.user1.has_perm('change', self.obj_foo), False)


        self.assertEquals(add_obj_permissions_to_user(self.obj_foo, ['view'], self.user1), True)
        self.user1 = User.objects.get(id=self.user1.id)
        self.assertEquals(ObjectPermission.objects.count(), 1)
        self.assertEquals(self.user1.has_perm('view', self.obj_foo), True)
        self.assertEquals(self.user1.has_perm('change', self.obj_foo), False)

    def test_add_permission(self):
        register_obj_permission(TestObjFoo, 'view')
        register_obj_permission(TestObjFoo, 'change')
        register_obj_permission(TestObjFoo, 'delete')
        
        # create permissions with the add_permissions function
        add_obj_permissions_to_user(self.obj_foo, ['view'], self.user1)
        
        self.user1 = User.objects.get(id=self.user1.id)
        self.assertEquals(ObjectPermission.objects.count(), 1)
        self.assertEquals(self.user1.has_perm('view', self.obj_foo), True)
        self.assertEquals(self.user1.has_perm('change', self.obj_foo), False)
        
        add_obj_permissions_to_user(self.obj_foo, ['change'], self.user1)
        
        self.user1 = User.objects.get(id=self.user1.id)
        self.assertEquals(ObjectPermission.objects.count(), 1)
        self.assertEquals(self.user1.has_perm('view', self.obj_foo), True)
        self.assertEquals(self.user1.has_perm('change', self.obj_foo), True)

        self.assertNotEquals(self.user1.has_perm('delete', self.obj_foo), True)
        self.assertNotEquals(self.user2.has_perm('view', self.obj_foo), True)
        self.assertNotEquals(self.user2.has_perm('change', self.obj_foo), True)
        self.assertNotEquals(self.user2.has_perm('delete', self.obj_foo), True)

    def test_add_obj_permissions_to_group(self):
        register_obj_permission(TestObjFoo, 'view')
        register_obj_permission(TestObjFoo, 'change')
        register_obj_permission(TestObjFoo, 'delete')
        
        group = Group.objects.create(name='Group1')
        
        self.assertEquals(add_obj_permissions_to_group(self.obj_foo, ['view'], group), True)
        add_user_to_group(self.user1, group)

        
        #self.user1 = User.objects.get(id=self.user1.id)
        self.assertEquals(UserPermissionList.objects.count(), 1)
        self.assertEquals(GroupObjectPermission.objects.count(), 1)
        self.assertEquals(self.user1.has_perm('view', self.obj_foo), True)
        
        # check permission cache usuage
        self.assertEquals(self.user1.has_perm('view', self.obj_foo), True)
        self.assertEquals(self.user1.has_perm('view', self.obj_foo), True)
        self.assertEquals(self.user1.has_perm('invalid', self.obj_foo), False)

    def test_object_permission_unicode_method(self):
        test_obj = TestObjFoo()
        test_obj.id = 1
        
        user_perm_obj = ObjectPermission.objects.create(user_id=self.user1.id, object_id=test_obj.id, content_type=get_content_type_string(test_obj))

        self.assertEquals('%s:%s:%i'%(self.user1.id, get_content_type_string(test_obj), test_obj.id), user_perm_obj.__unicode__())

    def test_group_object_permission_unicode_method(self):
        test_obj = TestObjFoo()
        test_obj.id = 1
        group = Group.objects.create(name='Group1')
        
        group_perm_obj = GroupObjectPermission.objects.create(group_id=group.id, object_id=test_obj.id, content_type=get_content_type_string(test_obj))

        self.assertEquals('%s:%s:%i'%(group.id, get_content_type_string(test_obj), test_obj.id), group_perm_obj.__unicode__())

    def test_permission_type__unicode_method(self):
        permission_type = PermissionType.objects.create(content_type=get_content_type_string(TestObjFoo()), permission_name='foo')
        
        self.assertEquals('%s:%s'%(get_content_type_string(TestObjFoo()), 'foo'), permission_type.__unicode__())
        












































































































































































































































































































































































































































































