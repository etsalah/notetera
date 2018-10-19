import os
from datetime import datetime
from sanic import Blueprint
from sanic.response import json
from models.v1.user import User
from helpers import query_helper
from helpers import command_helper
from helpers import param_helper
from helpers import id_helper
from helpers import password_helper
from helpers import jwt_helper
from decorations.session_helper import inject_session
from decorations.authentication_helper import authenticate
user_bp = Blueprint('user_blue_print', url_prefix='/v1/user')



@user_bp.get('/')
@authenticate()
@inject_session()
async def user_index(request, session_obj, user_obj):
    params = param_helper.get_json(request, True)
    pagination_args = param_helper.get_pagination_details(request)
    result = query_helper.list_query(
        session_obj, User, params, pagination_args, True)
    return json(result)


@user_bp.post('/')
@inject_session()
async def save_user(request, session_obj):
    data = param_helper.get_json(request)
    _id = id_helper.generate_id()
    data.update({
        'ver': _id, 'id': _id,
        'password': password_helper.encrypt(data['password']),
        'created_at': datetime.utcnow()
    })
    result = command_helper.save(
        session_obj, User, User.COLUMNS, data, json_result=True)
    session_obj.commit()
    return json(result)


@user_bp.post('/login')
@inject_session()
async def login(request, session_obj):
    params = param_helper.get_json(request)
    if 'password' in params:
        params.update({'password': password_helper.encrypt(params['password'])})

    args = [
        {"username": {"$eq": params['username']}},
        {"password": {"$eq": params['password']}}
    ]
    result = query_helper.find_by_params(session_obj, User, args, True)
    if result:
        result.update({"token": jwt_helper.encode_token(result)})
        return json(result)
    return json({'message': 'invalid login details'}, 401)


@user_bp.get('/<user_id>')
@inject_session()
@authenticate()
async def find_user(request, session_obj, user_obj, user_id):
    result = query_helper.find_by_id(session_obj, User, user_id, True)
    return json(result)


@user_bp.get('/count')
@inject_session()
@authenticate()
async def count(request, session_obj, user_obj):
    params = param_helper.get_json(request, remove_token=True)
    result = query_helper.count(session_obj, User, params)
    return json(result)
