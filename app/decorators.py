from functools import wraps
from flask import request
from flask_api.exceptions import PermissionDenied


def authorize_admin_users_only(func):
    """
    decorator function used to deny access
    for non-admin users on api endpoints

    :param func:
    :return:
    """
    @wraps(func)
    def wrapped_route(*args, **kwargs):
        if request.headers.get("X-ADMIN") != '1':
            raise PermissionDenied
        return func(*args, **kwargs)

    return wrapped_route
