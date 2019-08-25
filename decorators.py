from functools import wraps

import jwt
from flask import request, abort, current_app

from core.helpers.user_helper import has_permission


def get_user_info(fn):
    @wraps(fn)
    def inner_function(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        try:
            token_data = jwt.decode(request.headers['Authorization'], current_app.config['SECRET_KEY'])
        except:
            abort(401)

        return fn(token_data=token_data, *args, **kwargs)

    return inner_function


def login_required(permission=None):
    def decorator(fn):
        @wraps(fn)
        @get_user_info
        def inner_function(*args, **kwargs):
            token_data = kwargs.pop('token_data', None)
            current_app.logger.info(token_data)
            if token_data and permission:
                if not has_permission(token_data['sub'], permission):
                    abort(403)

            return fn(token_data=token_data, *args, **kwargs)

        return inner_function

    return decorator
