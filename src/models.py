from typing import List

from bson import ObjectId
from pydantic import BaseModel

from config.db import get_collection


class SurveyResult(BaseModel):
    question_number: int
    question_value: int


class SurveyResponse(BaseModel):
    user_id: str
    survey_results: List[SurveyResult]
    overall_analysis: str
    cat_dog: str
    fur_value: str
    tail_value: str
    description: str


async def insert_survey_response(survey_response: SurveyResponse):
    collection = get_collection("survey_responses")
    response_data = survey_response.dict(by_alias=True)
    response_data["_id"] = ObjectId()
    await collection.insert_one(response_data)


async def get_survey_response(user_id: str):
    collection = get_collection("survey_responses")
    return await collection.find_one({"user_id": user_id})
