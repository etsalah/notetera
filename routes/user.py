from sanic import Blueprint
from sanic.response import json

user_bp = Blueprint('user_blue_print', url_prefix='/user')

@user_bp.route('/')
async def user_index(request):
    return json({'endpoint': 'user blueprint'})