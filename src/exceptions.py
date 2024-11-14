import logging
from json.decoder import JSONDecodeError
from typing import Any, Dict, List

from pydantic import ValidationError
from sanic import NotFound, response
from sanic.exceptions import SanicException


class SurveyProcessingError(SanicException):
    status_code = 400


class DatabaseError(SanicException):
    status_code = 500


# Error Response Formatter
def format_validation_errors(e: ValidationError) -> List[Dict[str, Any]]:
    return [{"field": err["loc"][0], "message": err["msg"]} for err in e.errors()]


# Generalized response function for errors
def create_error_response(message: str, status: int = 400, extra_info: dict = None):
    """
    Creates a standard error response.
    """
    return response.json(
        {"status": "error", "message": message, **(extra_info if extra_info else {})},
        status=status,
    )


# General Error Response Handler
async def handle_exception(request, exception):
    if isinstance(exception, NotFound):
        # return response.json({"error": "URL not found"}, status=404)
        return await response.file("templates/not_found.html")

    if isinstance(exception, ValidationError):
        errors = format_validation_errors(exception)
        return response.json({"status": "error", "errors": errors}, status=400)

    elif isinstance(exception, SurveyProcessingError):
        logging.error("Survey processing error: %s", exception)
        return response.json({"status": "error", "message": str(exception)}, status=400)

    elif isinstance(exception, DatabaseError):
        logging.error("Database error: %s", exception)
        return response.json(
            {"status": "error", "message": "Database operation failed"}, status=500
        )

    elif isinstance(exception, JSONDecodeError):
        return create_error_response(
            "Malformed JSON in the request. Please check the payload.", status=400
        )

    elif isinstance(exception, KeyError):
        return create_error_response(
            f"Missing key: {str(exception)} in the request payload.", status=400
        )

    elif isinstance(exception, TypeError):
        return create_error_response(
            "Invalid data type in the request payload.", status=400
        )

    elif isinstance(exception, ValueError):
        return create_error_response(
            "Invalid value in the request payload.", status=400
        )

    elif isinstance(exception, TimeoutError):
        return create_error_response(
            "The operation timed out. Please try again later.", status=408
        )

    elif isinstance(exception, AttributeError):
        return create_error_response(
            "Expected attribute is missing in the request payload.", status=400
        )

    else:
        logging.critical("Unhandled exception: %s", exception, exc_info=True)
        return response.json(
            {"status": "error", "message": "An unexpected error occurred"}, status=500
        )
