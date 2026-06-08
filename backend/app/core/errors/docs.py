"""
Reusable OpenAPI error response declarations.
"""

from app.api.schemas.error import ErrorResponse


STANDARD_ERROR_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Bad Request"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    403: {"model": ErrorResponse, "description": "Forbidden"},
    404: {"model": ErrorResponse, "description": "Not Found"},
    409: {"model": ErrorResponse, "description": "Conflict"},
    422: {"model": ErrorResponse, "description": "Validation Error"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
}