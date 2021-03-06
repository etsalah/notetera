import os
from dotenv import load_dotenv
from sanic import Sanic, response
from sanic.response import json
from routes.v1.user import user_bp as user_bp_v1
from routes.v1.status import status_bp as status_bp_v1
from routes.v1.label import label_bp as label_bp_v1
from routes.v1.note import note_bp as note_bp_v1
from routes.v1.note_status import note_status_bp as note_status_bp_v1
from routes.v1.note_label import note_label_bp as note_label_bp_v1
from models.v1.base import create_engine
from models.v1.base import create_db_entities
from models.v1.base import create_session
from models.v1.user import User
from models.v1.note import Note
from models.v1.status import Status
from models.v1.label import Label
from helpers import query_helper
from sanic_cors import CORS

load_dotenv()


def init_app():
    conn_str = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
        os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'),
        os.getenv('DB_HOST'), os.getenv('DB_DATABASE')
    )
    os.environ['conn_str'] = conn_str
    db_engine = create_engine(conn_str, echo=True)
    session_obj = create_session(db_engine)
    create_db_entities(db_engine)

    query_helper.FIELD_MODEL_MAPPING = {
        'created_by_id': {'cls': User, 'label': 'created_by'},
        'parent_note_id': {'cls': Note, 'label': 'parent_note'},
        'status_id': {'cls': Status, 'label': 'status'},
        'label_id': {'cls': Label, 'label': 'label'},
        'note_id': {'cls': Note, 'label': 'note'}
    }


app = Sanic(__name__)

CORS(app)


ROUTES = [
    user_bp_v1, status_bp_v1, label_bp_v1, note_bp_v1, note_status_bp_v1,
    note_label_bp_v1
]

for route in ROUTES:
    app.blueprint(route)


init_app()


@app.route('/')
async def test(request):
    return json({"hello": "world"})
