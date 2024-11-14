import logging
from statistics import mean, median, stdev
from typing import Dict, List

import aiofiles
import openai

from config.settings import settings
from src.exceptions import SurveyProcessingError
from src.fallback_description import get_fallback_description
from src.validation import SurveyData

# Initialize OpenAI API key
openai.api_key = settings.OPENAI_API_KEY


logger = logging.getLogger("SurveyApp")


async def process_survey_data(survey_data: SurveyData) -> Dict:

    try:

        overall_analysis = (
            "certain"
            if survey_data.survey_results[0].question_value != 7
            or survey_data.survey_results[3].question_value >= 3
            else "unsure"
        )

        cat_dog = (
            "cats"
            if survey_data.survey_results[9].question_value > 5
            and survey_data.survey_results[8].question_value <= 5
            else "dogs"
        )

        average_value = sum(
            [item.question_value for item in survey_data.survey_results]
        ) / len(survey_data.survey_results)

        fur_value = "long" if average_value > 4 else "short"

        # Determine tail_value based on question number 7
        tail_value = (
            "long" if survey_data.survey_results[6].question_value > 4 else "short"
        )

        description = await generate_description(average_value)

        return {
            "overall_analysis": overall_analysis,
            "cat_dog": cat_dog,
            "fur_value": fur_value,
            "tail_value": tail_value,
            "description": description,
        }

    except Exception as e:
        logger.error("Error processing survey data: %s", e)
        raise SurveyProcessingError("Survey data processing failed.")


async def calculate_statistics(question_values: List[int]) -> dict:
    try:

        if not question_values:
            raise ValueError("question_values cannot be empty")
        return {
            "mean": round(mean(question_values), 2),
            "median": round(median(question_values), 2),
            "std_dev": (
                round(stdev(question_values), 2) if len(question_values) > 1 else 0
            ),
        }
    except ValueError as e:
        logger.error("Statistics calculation error: %s", e)
        raise SurveyProcessingError("Invalid data for statistics calculation.")


async def read_file(file_path: str) -> str:
    """
    Reads the contents of a text file asynchronously.
    """
    async with aiofiles.open(file_path, mode="r") as f:
        text = await f.read()
    return text


# API call to OpenAI to generate description
async def generate_description_from_api(is_short_hair: bool):
    """Generate description using OpenAI API."""

    file_name = (
        "the_value_of_short_hair.txt" if is_short_hair else "the_value_of_long_hair.txt"
    )
    content_file_path = f"templates/{file_name}"
    system_prompt_file_path = f"templates/{file_name}"

    #     # Load content
    content = await read_file(content_file_path)

    #     # Load system prompt
    system_prompt = await read_file(system_prompt_file_path)

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content},
            ],
        )
        return response.choices[0].message
    except Exception as e:
        logger.error(f"API request failed: {str(e)}")
        return None


async def generate_description(average_value: float) -> str:
    # Choose the correct file based on the average value
    is_short_hair = average_value > 4

    # Try to get description from OpenAI
    description = await generate_description_from_api(is_short_hair)
    if not description:
        description = get_fallback_description(is_short_hair)

    return description
