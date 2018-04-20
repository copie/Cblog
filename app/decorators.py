from functools import wraps

from flask import abort, current_app
from .models import Permission
from flask_login import current_user


def permission_required(permissios):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            if not current_user.can(permissios):
                abort(403)
            return f(*args, **kwargs)
        return decorator_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
