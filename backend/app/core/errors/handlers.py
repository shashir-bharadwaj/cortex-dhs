"""
Global FastAPI exception handlers.

This module converts framework-level and application-level exceptions into
one standard API error response shape.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.schemas.error import ErrorDetail, ErrorResponse
from app.core.errors.base import AppException
from app.core.errors.codes import ErrorCodes
from app.core.errors.messages import ErrorMessages

logger = logging.getLogger(__name__)


def _build_error_response(
    *,
    error_code: str,
    message: str,
    path: str,
    details: list[dict] | None = None,
    meta: dict | None = None,
) -> dict:
    """
    Build a serialized standard error response payload.
    """
    response = ErrorResponse(
        error_code=error_code,
        message=message,
        details=[
            ErrorDetail(
                field=item.get("field"),
                message=item.get("message", "Unknown error."),
                code=item.get("code"),
            )
            for item in (details or [])
        ],
        path=path,
        meta=meta,
    )
    return response.model_dump(mode="json")


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all custom/global exception handlers on the FastAPI app.
    """

    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException) -> JSONResponse:
        """
        Handle known application exceptions.
        """
        logger.warning(
            "Application exception raised",
            extra={
                "error_code": exc.error_code,
                "path": request.url.path,
                "meta": exc.meta,
            },
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=_build_error_response(
                error_code=exc.error_code,
                message=exc.message,
                path=request.url.path,
                details=exc.details,
                meta=exc.meta,
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """
        Handle FastAPI/Pydantic request validation failures.
        """
        details = []

        for error in exc.errors():
            location = [
                str(item)
                for item in error.get("loc", [])
                if item not in {"body", "query", "path"}
            ]

            details.append(
                {
                    "field": ".".join(location) if location else None,
                    "message": error.get("msg", "Invalid request."),
                    "code": error.get("type"),
                }
            )

        return JSONResponse(
            status_code=422,
            content=_build_error_response(
                error_code=ErrorCodes.REQUEST_VALIDATION_ERROR,
                message=ErrorMessages.REQUEST_VALIDATION_FAILED,
                path=request.url.path,
                details=details,
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(
        request: Request,
        exc: StarletteHTTPException,
    ) -> JSONResponse:
        """
        Normalize framework HTTP exceptions into the standard format.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content=_build_error_response(
                error_code=f"HTTP_{exc.status_code}",
                message=str(exc.detail),
                path=request.url.path,
            ),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Catch all unexpected exceptions to avoid leaking internal details.
        """
        logger.exception("Unhandled exception occurred", exc_info=exc)

        return JSONResponse(
            status_code=500,
            content=_build_error_response(
                error_code=ErrorCodes.INTERNAL_SERVER_ERROR,
                message=ErrorMessages.INTERNAL_SERVER_ERROR,
                path=request.url.path,
            ),
        )