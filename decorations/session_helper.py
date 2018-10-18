import os
from functools import wraps
from models.v1.base import create_session_from_conn_str

session_obj = None

def inject_session():

    def decorator(f):

        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            global session_obj
            if not session_obj:
                session_obj = create_session_from_conn_str(
                    os.getenv('conn_str'), False)
            kwargs['session_obj'] = session_obj
            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator
