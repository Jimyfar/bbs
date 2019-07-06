import uuid
from functools import wraps

from flask import (
    request,
    redirect,
    url_for,
    abort,
)

from models.user import User
import redis

from utils import log

cache = redis.StrictRedis()


def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        uid = cache.get(session_id)
        if uid is not None:
            u = User.one(id=uid)
            if u is None:
                return User.guest()
            else:
                return u
    else:
        return User.one(id=1)


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        k = 'csrf_token_{}'.format(u.id)
        if cache.exists(k):
            cache.delete(k)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    log('new_csrf_token, user', u)
    token = str(uuid.uuid4())
    k = 'csrf_token_{}'.format(u.id)
    cache.set(k, token)
    return token


def new_session(user_id):
    token = str(uuid.uuid4())
    k = 'session_id_{}'.format(token)
    cache.set(k, user_id)
    log('k', k,'user_id', user_id)
    return k
