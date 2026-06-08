from app.core.errors.base import AppException
from app.core.errors.codes import ErrorCodes
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.core.errors.exceptions import (
    BusinessRuleError,
    ConflictError,
    DeviceAlreadyAssignedError,
    DeviceAlreadyExistsError,
    DeviceAssignmentNotAllowedError,
    DeviceNotFoundError,
    ForbiddenError,
    PatientNotFoundError,
    ResourceNotFoundError,
    UnauthorizedError,
    ValidationAppError,
)
from app.core.errors.handlers import register_exception_handlers

__all__ = [
    "AppException",
    "ErrorCodes",
    "STANDARD_ERROR_RESPONSES",
    "BusinessRuleError",
    "ConflictError",
    "DeviceAlreadyAssignedError",
    "DeviceAlreadyExistsError",
    "DeviceAssignmentNotAllowedError",
    "DeviceNotFoundError",
    "ForbiddenError",
    "PatientNotFoundError",
    "ResourceNotFoundError",
    "UnauthorizedError",
    "ValidationAppError",
    "register_exception_handlers",
]