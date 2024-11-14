from unittest import mock

import pytest

from src.logic import generate_description


@pytest.mark.asyncio
async def test_generate_description_short_hair_api_success(mocker):
    # Mock API response for a successful API call for short hair
    mock_response = mock.Mock()
    mock_response.choices = [
        mock.Mock(message="API-generated description for short hair")
    ]
    mocker.patch("src.logic.openai.chat.completions.create", return_value=mock_response)
    description = await generate_description(average_value=5)

    assert description == "API-generated description for short hair"


@pytest.mark.asyncio
async def test_generate_description_long_hair_api_success(mocker):
    # Mock API response for a successful API call for long hair
    mock_response = mock.Mock()
    mock_response.choices = [
        mock.Mock(message="API-generated description for long hair")
    ]
    mocker.patch("src.logic.openai.chat.completions.create", return_value=mock_response)
    description = await generate_description(average_value=3)
    assert description == "API-generated description for long hair"


@pytest.mark.asyncio
async def test_generate_description_short_hair_api_failure_fallback(mocker):
    # Mock API response to fail and return None
    mocker.patch(
        "src.logic.openai.chat.completions.create", side_effect=Exception("API error")
    )
    mocker.patch(
        "src.fallback_description.random.choice",
        return_value="Fallback description for short hair",
    )
    description = await generate_description(average_value=5)
    assert description == "Fallback description for short hair"


@pytest.mark.asyncio
async def test_generate_description_long_hair_api_failure_fallback(mocker):
    # Mock API response to fail and return None
    mocker.patch(
        "src.logic.openai.chat.completions.create", side_effect=Exception("API error")
    )
    mocker.patch(
        "src.fallback_description.random.choice",
        return_value="Fallback description for long hair",
    )
    description = await generate_description(average_value=3)
    assert description == "Fallback description for long hair"


@pytest.mark.asyncio
async def test_generate_description_api_none_response_fallback(mocker):
    # Mock API response to return None
    mock_response = mock.Mock()
    mock_response.choices = [mock.Mock(message=None)]
    mocker.patch("src.logic.openai.chat.completions.create", return_value=mock_response)
    mocker.patch(
        "src.fallback_description.random.choice",
        return_value="Fallback description when API response is None",
    )

    # Run the function with a value to trigger either short or long hair
    description = await generate_description(average_value=5)

    # Assert that the fallback description is returned
    assert description == "Fallback description when API response is None"
