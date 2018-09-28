from sanic import Sanic
from sanic.response import json
from routes.v1.user import user_bp as user_bp_v1
from routes.v1.status import status_bp as status_bp_v1
from routes.v1.label import label_bp as label_bp_v1
from routes.v1.note import note_bp as note_bp_v1

app = Sanic()

ROUTES = [
    user_bp_v1, status_bp_v1, label_bp_v1, note_bp_v1
]

for route in ROUTES:
    app.blueprint(route)


@app.route('/')
async def test(request):
    return json({"hello": "world"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
