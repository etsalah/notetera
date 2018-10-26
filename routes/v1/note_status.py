from datetime import datetime
from sanic import Blueprint
from sanic.response import json
from models.v1.note_status import NoteStatus
from decorations.authentication_helper import authenticate
from decorations.session_helper import inject_session
from decorations.exception_helper import handle_exception
from helpers import param_helper, query_helper, command_helper
from helpers import id_helper


note_status_bp = Blueprint(
	'note_status_blue_print', url_prefix='/v1/note/<note_id>/status')


@note_status_bp.get('/')
@inject_session()
@authenticate()
@handle_exception()
async def note_status_index(request, session_obj, user_obj, note_id):
    params = param_helper.get_json(request)
    filters = params.get('filters', [])
    filters.extend([
    	{'created_by_id': {"$eq": user_obj['id']}},
    	{'note_id': {'$eq': note_id}}
	])
    pagination_args = param_helper.get_pagination_details(request)
    result = query_helper.list_query(
        session_obj, NoteStatus, filters, pagination_args, json_result=True)
    return json(result)


@note_status_bp.get('/count')
@inject_session()
@authenticate()
@handle_exception()
async def count_note_status(request, session_obj, user_obj, note_id):
    params = param_helper.get_json(request)
    filters = params.get('filters', [])
    filters.extend([
    	{'created_by_id': {"$eq": user_obj['id']}},
    	{'note_id': {'$eq': note_id}}
	])
    return json(query_helper.count(session_obj, NoteStatus, filters))


@note_status_bp.get('/<status_id>')
@inject_session()
@authenticate()
@handle_exception()
async def find_note_status(request, session_obj, user_obj, status_id, note_id):
    filters = [
        {'id': {'$eq': status_id}},
        {'created_by_id': {'$eq': user_obj['id']}}
    ]
    return json(
        query_helper.find_by_params(
            session_obj, NoteStatus, filters, json_result=True))


@note_status_bp.put('/<status_id>')
@inject_session()
@authenticate()
@handle_exception()
async def update_note_status(request, session_obj, user_obj, status_id):
    params = param_helper.get_json(request)
    filters = params.get('filters', [])
    filters.extend([
        {'id': {'$eq': status_id}},
        {'created_by_id': {'$eq': user_obj['id']}}
    ])
    data = {'ver': id_helper.generate_id(), 'updated_at': datetime.utcnow()}
    for field in params.keys():
        if field not in ('id', 'ver', 'created_by_id'):
            data[field] = params[field]
    result = command_helper.update_by_params(
        session_obj, NoteStatus, filters, data, json_result=True)
    session_obj.commit()
    return json(result)


@note_status_bp.delete('/<status_id>')
@inject_session()
@authenticate()
@handle_exception()
async def delete_note_status(request, session_obj, user_obj, status_id):
    params = param_helper.get_json(request)
    filters = params.get('filters', [])  # TODO: make sure that ver is passed
    filters.extend([
        {'id': {'$eq': status_id}},
        {'created_by_id': {'$eq': user_obj['id']}}
    ])

    data = {'ver': id_helper.generate_id(), 'deleted_at': datetime.utcnow()}
    for field in params.keys():
        if field not in ('id', 'ver', 'name', 'created_by_id'):
            data[field] = params[field]
    result = command_helper.delete_by_params(
        session_obj, NoteStatus, filters, data, json_result=True)
    session_obj.commit()
    return json(result)


@note_status_bp.post('/')
@inject_session()
@authenticate()
@handle_exception()
async def create_note_status(request, session_obj, user_obj, note_id):
    params = param_helper.get_json(request)
    _id = id_helper.generate_id()
    params.update({
        'created_at': datetime.utcnow(), 'id': _id,
        'ver': _id, 'created_by_id': user_obj['id'],
        'note_id': note_id
    })
    result = command_helper.save(
        session_obj, NoteStatus, NoteStatus.COLUMNS, params, json_result=True)

    session_obj.commit()
    return json(result)

