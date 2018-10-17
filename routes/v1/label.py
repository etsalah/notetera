from sanic import Blueprint
from sanic.response import json
from models.v1.label import Label

label_bp = Blueprint('label_blue_print', url_prefix='/v1/label')

@label_bp.route('/')
async def label_index(request):
    return json({'endpoint': 'label blueprint'})
