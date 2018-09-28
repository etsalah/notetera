from sanic import Blueprint
from sanic.response import json

note_bp = Blueprint('note_blue_print', url_prefix='/v1/note')

@note_bp.route('/')
async def note_index(request):
    return json({'endpoint': 'note blueprint'})
