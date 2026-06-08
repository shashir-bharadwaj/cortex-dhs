"""
Base application exception hierarchy.

All business/application/domain exceptions should inherit from AppException.
These exceptions remain framework-agnostic and are translated into HTTP
responses only at the API layer via global FastAPI handlers.
"""

from typing import Any, Dict, List, Optional

from app.core.errors.codes import ErrorCodes


class AppException(Exception):
    """
    Base exception for known application errors.

    Attributes:
        message: Human-readable top-level message.
        error_code: Stable machine-readable code for frontend/backend use.
        status_code: HTTP status code to be used by the global handler.
        details: Optional structured detail list.
        meta: Optional structured metadata.
    """

    def __init__(
        self,
        message: str,
        *,
        error_code: str = ErrorCodes.INTERNAL_SERVER_ERROR,
        status_code: int = 500,
        details: Optional[List[Dict[str, Any]]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or []
        self.meta = meta

        super().__init__(message)