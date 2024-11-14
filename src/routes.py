from pydantic import ValidationError
from sanic import Blueprint, response

from src.exceptions import handle_exception
from src.models import SurveyResponse, insert_survey_response

from .logic import calculate_statistics, process_survey_data
from .validation import SurveyData

# Create a Blueprint for the survey routes
bp = Blueprint("survey_blueprint")


# Landing page route
@bp.route("/", methods=["GET"])
async def landing_page(request):
    return await response.file("templates/index.html")


@bp.route("/process-survey", methods=["POST"])
async def process_survey(request):
    """
    Endpoint to process survey data. Expects JSON payload.
    """
    try:
        # Validate incoming data with Pydantic model
        survey_data = SurveyData(**request.json)

        analysis = await process_survey_data(survey_data)

        question_values = [item.question_value for item in survey_data.survey_results]
        stats = await calculate_statistics(question_values)

        survey_results = [item.dict() for item in survey_data.survey_results]

        survey_response = SurveyResponse(
            user_id=survey_data.user_id,
            survey_results=survey_results,
            overall_analysis=analysis.get("overall_analysis"),
            cat_dog=analysis.get("cat_dog"),
            fur_value=analysis.get("fur_value"),
            tail_value=analysis.get("tail_value"),
            description=analysis.get("description"),
        )

        # Store survey response in DB
        await insert_survey_response(survey_response)

        return response.json(
            {
                "status": "success",
                "message": "Survey processed successfully",
                "analysis": analysis,
                "statistics": stats,
            },
            status=200,
        )

    except ValidationError as e:
        # Custom error response
        errors = [{"field": err["loc"][0], "message": err["msg"]} for err in e.errors()]
        return response.json({"status": "error", "errors": errors}, status=400)

    except Exception as e:
        # Handle exception by calling the centralized handler
        return handle_exception(e)
