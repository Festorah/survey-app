import pytest

from src.logic import calculate_statistics, process_survey_data
from src.validation import SurveyData, SurveyResult


@pytest.mark.asyncio
async def test_calculate_statistics():
    question_values = [4, 5, 6, 4, 5, 6, 5, 4, 6, 5]
    stats = await calculate_statistics(question_values)
    assert stats["mean"] == 5
    assert stats["median"] == 5
    assert stats["std_dev"] == 0.82
    assert "std_dev" in stats  # Check standard deviation is calculated


@pytest.mark.asyncio
async def test_process_survey_data():
    survey_data = SurveyData(
        user_id="test_user",
        survey_results=[
            SurveyResult(question_number=i, question_value=5) for i in range(1, 11)
        ],
    )
    analysis = await process_survey_data(survey_data)
    assert analysis["overall_analysis"] is not None
    assert "cat_dog" in analysis
    assert "fur_value" in analysis
    assert "tail_value" in analysis
