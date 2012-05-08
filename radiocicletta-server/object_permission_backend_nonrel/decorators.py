from functools import wraps
from django.core.exceptions import PermissionDenied

def obj_permission_required(permission, get_obj_func, params=None):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            obj = get_obj_func(request, *args, **kwargs)
            if request.user.has_perm(permission, obj):
                kwargs['obj'] = obj
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wraps(view_func) (_wrapped_view)
    return decorator
                                         
