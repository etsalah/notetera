import os
from functools import wraps
from helpers import jwt_helper
from helpers import param_helper
from sanic.response import json
from jwt.exceptions import ExpiredSignatureError, DecodeError


def authenticate():

    def decorator(f):

        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            params = param_helper.get_json(request, remove_token=False)

            if not params or 'token' not in params:
                return json(
                    {'message': 'you need to pass in access token'}, 401)
            
            try:
                user_obj = jwt_helper.decode_token(params, 'token')

                kwargs['user_obj'] = user_obj
                return await f(request, *args, **kwargs)
            except ExpiredSignatureError:
                return json({
                    'message': 'Your login has expired, please login again'
                    }, 401)
            except DecodeError:
                return json({
                    'message': (
                        'Your token is invalid, provide a valid token '
                        'to proceed')
                    }, 401)

        return decorated_function

    return decorator

