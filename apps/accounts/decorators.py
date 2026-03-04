from functools import wraps
from django.core.exceptions import PermissionDenied


def role_required(allowed_roles):
    """Decorator to allow only users with a role in allowed_roles or superuser."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                raise PermissionDenied()
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            if getattr(user, 'role', None) in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied()
        return _wrapped
    return decorator
