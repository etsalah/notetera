import os
from dotenv import load_dotenv
from sanic import Sanic
from sanic.response import json
from routes.v1.user import user_bp as user_bp_v1
from routes.v1.status import status_bp as status_bp_v1
from routes.v1.label import label_bp as label_bp_v1
from routes.v1.note import note_bp as note_bp_v1
from models.v1.base import create_engine
from models.v1.base import create_db_entities
from models.v1.base import create_session
# from helpers import jwt_helper
# import models.v1 as v1_models

load_dotenv()

session_obj = None
def init_app():
    global session_obj
    conn_str = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
        os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'),
        os.getenv('DB_HOST'), os.getenv('DB_DATABASE')
    )
    db_engine = create_engine(conn_str, echo=True)
    session_obj = create_session(db_engine)
    create_db_entities(db_engine)


app = Sanic()

ROUTES = [
    user_bp_v1, status_bp_v1, label_bp_v1, note_bp_v1
]

for route in ROUTES:
    app.blueprint(route)


init_app()


@app.route('/')
async def test(request):
    return json({"hello": "world"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
