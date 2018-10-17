from sanic import Blueprint
from sanic.response import json
from models.v1.status import Status

status_bp = Blueprint('status_blue_print', url_prefix='/v1/status')

@status_bp.route('/')
async def status_index(request):
    return json({'endpoint': 'status blueprint'})
