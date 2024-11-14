import pytest
from pydantic import ValidationError

from src.validation import SurveyData


def test_survey_data_valid():
    valid_data = {
        "user_id": "user_12345",
        "survey_results": [
            {"question_number": i, "question_value": 5} for i in range(1, 11)
        ],
    }
    survey_data = SurveyData(**valid_data)
    assert survey_data.user_id == "user_12345"
    assert len(survey_data.survey_results) == 10


def test_survey_data_invalid_question_value():
    invalid_data = {
        "user_id": "user_12345",
        "survey_results": [{"question_number": 1, "question_value": 10}],
    }
    with pytest.raises(ValidationError):
        SurveyData(**invalid_data)


def test_survey_data_missing_questions():
    incomplete_data = {
        "user_id": "user_12345",
        "survey_results": [
            {"question_number": i, "question_value": 5} for i in range(1, 9)
        ],
    }
    with pytest.raises(ValidationError):
        SurveyData(**incomplete_data)


def test_survey_data_duplicate_question_numbers():
    duplicate_data = {
        "user_id": "user_12345",
        "survey_results": [{"question_number": 1, "question_value": 5}] * 10,
    }
    with pytest.raises(ValidationError):
        SurveyData(**duplicate_data)
