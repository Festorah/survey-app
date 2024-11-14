import pytest
from sanic import Sanic
from sanic_testing import TestManager

from src.routes import bp as survey_blueprint


# Create the Sanic app instance with the blueprint registered
@pytest.fixture
def app():
    app = Sanic("test_survey_app")
    app.blueprint(survey_blueprint)
    TestManager(app)  # Add testing manager
    return app


@pytest.mark.asyncio
async def test_landing_page(app):
    request, response = await app.asgi_client.get("/")
    assert response.status == 200
    assert "text/html" in response.content_type


@pytest.mark.asyncio
async def test_process_survey_valid_payload(app):
    # Simulate a valid payload
    valid_payload = {
        "user_id": "user_12345",
        "survey_results": [
            {"question_number": i, "question_value": 4} for i in range(1, 11)
        ],
    }
    request, response = await app.asgi_client.post(
        "/process-survey", json=valid_payload
    )
    assert response.status == 200
    assert response.json["status"] == "success"
    assert "analysis" in response.json
    assert "statistics" in response.json


@pytest.mark.asyncio
async def test_process_survey_invalid_payload_missing_user_id(app):
    # Missing user_id
    invalid_payload = {
        "survey_results": [
            {"question_number": i, "question_value": 4} for i in range(1, 11)
        ],
    }
    request, response = await app.asgi_client.post(
        "/process-survey", json=invalid_payload
    )
    assert response.status == 400
    assert "status" not in response.json or response.json["status"] != "success"


@pytest.mark.asyncio
async def test_process_survey_invalid_payload_incorrect_values(app):
    # Invalid question_value (out of bounds)
    invalid_payload = {
        "user_id": "user_12345",
        "survey_results": [
            {"question_number": i, "question_value": 10} for i in range(1, 11)
        ],
    }
    request, response = await app.asgi_client.post(
        "/process-survey", json=invalid_payload
    )
    assert response.status == 400  # Expecting a validation error
    assert "status" not in response.json or response.json["status"] != "success"
