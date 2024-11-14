from unittest.mock import AsyncMock, patch

import pytest

from src.models import (
    SurveyResponse,
    SurveyResult,
    get_survey_response,
    insert_survey_response,
)


@pytest.mark.asyncio
@patch("src.models.get_collection")
async def test_insert_survey_response(mock_get_collection):
    # Create a mock collection with an async insert_one method
    mock_collection = AsyncMock()
    mock_get_collection.return_value = mock_collection
    mock_collection.insert_one = AsyncMock()

    # Define the survey response input data
    survey_response = SurveyResponse(
        user_id="test_user",
        survey_results=[
            SurveyResult(question_number=i, question_value=4) for i in range(1, 11)
        ],
        overall_analysis="unsure",
        cat_dog="dog",
        fur_value="long",
        tail_value="Short",
        description="Test Description",
    )

    # Call the function to test
    await insert_survey_response(survey_response)

    # Assert insert_one was called once with the expected data
    mock_collection.insert_one.assert_awaited_once()
    assert mock_collection.insert_one.call_args[0][0]["user_id"] == "test_user"


@pytest.mark.asyncio
@patch("src.models.get_collection")
async def test_get_single_survey_response_with_field_verification(mock_get_collection):
    mock_collection = AsyncMock()
    mock_get_collection.return_value = mock_collection

    # Define the expected document in the mock find_one return value
    mock_collection.find_one.return_value = {
        "user_id": "test_user",
        "survey_results": [{"question_number": 1, "question_value": 4}],
        "overall_analysis": "unsure",
        "cat_dog": "dog",
        "fur_value": "long",
        "tail_value": "Short",
        "description": "Test Description",
    }

    result = await get_survey_response("test_user")
    assert result is not None

    # Verify fields in the document
    assert "user_id" in result
    assert "survey_results" in result
    assert "overall_analysis" in result
    assert "cat_dog" in result
    assert "fur_value" in result
    assert "tail_value" in result
    assert "description" in result

    # Verify specific values
    assert result["user_id"] == "test_user"
    assert result["survey_results"] == [{"question_number": 1, "question_value": 4}]
    assert result["overall_analysis"] == "unsure"
    assert result["cat_dog"] == "dog"
    assert result["fur_value"] == "long"
    assert result["tail_value"] == "Short"
    assert result["description"] == "Test Description"

    # Ensure that find_one was called with the correct query
    mock_collection.find_one.assert_called_once_with({"user_id": "test_user"})
