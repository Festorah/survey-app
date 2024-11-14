from sanic import Sanic
from sanic.response import json

from src.main import app

app = Sanic("TestApp")
SanicTestClient = app.test_client


@app.route("/")
async def test(request):
    return json({"hello": "world"})


# Test for Sanic App Initialization
def test_app_initialization():
    assert app.name == "TestApp"
