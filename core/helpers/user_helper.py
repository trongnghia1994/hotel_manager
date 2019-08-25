import traceback
from datetime import datetime, timedelta

import jwt
from bson import ObjectId
from flask import current_app

from ..models import User, Role


def generate_token(sub):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
        'iat': datetime.utcnow(),
        'sub': sub
    }
    return jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
    )


def login_user(data):
    '''Authenticate user, if authenticated return token else return None'''
    email = data['email']
    password = data['password']
    user = None

    try:
        user = User.find_user(email, password)
    except:
        traceback.print_exc()

    result = {}
    if user:
        token = generate_token(str(user._id))
        result = {"user_id": str(user._id), "token": token}

    return result


def has_permission(user_id, permission_name):
    try:
        user = User.objects.get({'_id': ObjectId(user_id)})
    except:
        traceback.print_exc()
        user = None

    if user:
        if user.superuser:  # This is a superuser
            return True
        else:
            user_role = Role.objects.get({'_id': user.role})
            return permission_name in user_role.find_permissions()
    else:
        return False
