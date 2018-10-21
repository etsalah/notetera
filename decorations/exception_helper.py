import os
from functools import wraps
from helpers import jwt_helper
from helpers import param_helper
from sanic.response import json
from jwt.exceptions import ExpiredSignatureError, DecodeError
from sqlalchemy.exc import IntegrityError


def rollback(session_obj):
    if session_obj:
        session_obj.rollback()


def handle_exception():

    def decorator(f):

        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            session_obj = None
            
            if 'session_obj' in kwargs:
                session_obj = kwargs['session_obj']

            try:
                return await f(request, *args, **kwargs)
            except IntegrityError:
                rollback(session_obj)
                return json({
                    'message': (
                        'You have to make sure that entity you are creating '
                        'is unique')
                    }, 400)

        return decorated_function

    return decorator
