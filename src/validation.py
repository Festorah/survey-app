from typing import List

from pydantic import BaseModel, Field, field_validator


class SurveyResult(BaseModel):
    question_number: int = Field(
        ..., ge=1, le=10, description="Must be an integer between 1 and 10"
    )
    question_value: int = Field(
        ..., ge=1, le=7, description="Must be an integer between 1 and 7"
    )


class SurveyData(BaseModel):
    user_id: str = Field(
        ...,
        min_length=5,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Must be a string with at least 5 characters, alphanumeric and underscores allowed",
    )
    survey_results: List[SurveyResult] = Field(
        ...,
        min_length=10,
        max_length=10,
        description="Must contain exactly 10 survey result objects",
    )

    @field_validator("survey_results")
    def validate_question_numbers(cls, v):
        question_numbers = [item.question_number for item in v]
        if sorted(question_numbers) != list(range(1, 11)):
            raise ValueError(
                "Each question_number from 1 to 10 must appear exactly once."
            )
        return v
