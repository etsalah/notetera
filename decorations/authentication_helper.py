import os
from functools import wraps
from helpers import jwt_helper
from helpers import param_helper
from sanic.response import json

def authenticate():

    def decorator(f):

        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            params = param_helper.get_json(request)

            if not params or 'token' not in params:
                return json(
                    {'message': 'you need to pass in access token'}, 401)

            user_obj = jwt_helper.decode_token(params, 'token')

            kwargs['user_obj'] = user_obj
            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator

