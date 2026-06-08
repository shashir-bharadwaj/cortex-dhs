"""
Standard API error response schemas.

These schemas define one consistent error contract for the entire backend,
so frontend clients always receive the same structure regardless of module.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """
    Represents a fine-grained error item, typically field-level validation
    or a contextual business rule detail.
    """

    field: Optional[str] = Field(
        default=None,
        description="Field associated with the error, if applicable.",
    )
    message: str = Field(
        ...,
        description="Human-readable detail for the specific error item.",
    )
    code: Optional[str] = Field(
        default=None,
        description="Optional machine-readable sub-code for this detail.",
    )


class ErrorResponse(BaseModel):
    """
    Standard error response returned by all exception handlers.
    """

    success: bool = Field(
        default=False,
        description="Indicates that the request failed.",
    )
    error_code: str = Field(
        ...,
        description="Stable machine-readable top-level error code.",
    )
    message: str = Field(
        ...,
        description="Human-readable top-level error message.",
    )
    details: List[ErrorDetail] = Field(
        default_factory=list,
        description="Optional list of detailed error items.",
    )
    path: Optional[str] = Field(
        default=None,
        description="Request path where the error occurred.",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp of error generation.",
    )
    meta: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional structured metadata for debugging or UI behavior.",
    )