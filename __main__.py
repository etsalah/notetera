from sanic import Sanic
from sanic.response import json
from routes.user import user_bp

app = Sanic()

app.blueprint(user_bp)

@app.route('/')
async def test(request):
    return json({"hello": "world"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
