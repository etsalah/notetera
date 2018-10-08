from sanic import Blueprint
from sanic.response import json
from models.v1.user import User


user_bp = Blueprint('user_blue_print', url_prefix='/v1/user')

@user_bp.route('/')
async def user_index(request):
    return json({'endpoint': 'user blueprint'})
