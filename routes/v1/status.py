from datetime import datetime
from sanic import Blueprint
from sanic.response import json
from models.v1.status import Status
from decorations.authentication_helper import authenticate
from decorations.session_helper import inject_session
from helpers import param_helper, query_helper, command_helper
from helpers import id_helper


status_bp = Blueprint('status_blue_print', url_prefix='/v1/status')

@status_bp.get('/')
@inject_session()
@authenticate()
async def status_index(request, session_obj, user_obj):
    params = param_helper.get_json(request, remove_token=True)
    pagination_args = param_helper.get_pagination_details(request)
    return json(
        query_helper.list_query(
            session_obj, Status, params, pagination_args, True))


@status_bp.get('/<status_id>')
@inject_session()
@authenticate()
async def find_status(request, session_obj, user_obj, status_id):
    return json(
        query_helper.find_by_id(
            session_obj, Status, status_id, json_result=True))


@status_bp.get('/count')
@inject_session()
@authenticate()
async def count_status(request, session_obj, user_obj):
    return json({'endpoint': 'count status'})


@status_bp.post('/')
@inject_session()
@authenticate()
async def save_status(request, session_obj, user_obj):
    params = param_helper.get_json(request, True)
    _id = id_helper.generate_id()
    params.update({
        'id': _id, 'ver': _id,
        'created_at': datetime.utcnow(),
        'created_by_id': user_obj['id']
    })
    result = command_helper.save(
        session_obj, Status, Status.COLUMNS, params, json_result=True)
    session_obj.commit()
    return json(result)
