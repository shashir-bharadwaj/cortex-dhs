"""
Known application-specific exception types.

These classes map common failure categories to standard HTTP status codes
while keeping business logic decoupled from FastAPI.
"""

from typing import Any, Dict, List, Optional

from app.core.errors.base import AppException
from app.core.errors.codes import ErrorCodes
from app.core.errors.messages import ErrorMessages


class ValidationAppError(AppException):
    """
    Raised when application-level input or invariant validation fails.
    """

    def __init__(
        self,
        message: str = ErrorMessages.VALIDATION_FAILED,
        *,
        details: Optional[List[Dict[str, Any]]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=ErrorCodes.VALIDATION_ERROR,
            status_code=422,
            details=details,
            meta=meta,
        )


class ResourceNotFoundError(AppException):
    """
    Raised when a requested entity/resource does not exist.
    """

    def __init__(
        self,
        message: str = ErrorMessages.RESOURCE_NOT_FOUND,
        *,
        error_code: str = ErrorCodes.RESOURCE_NOT_FOUND,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=404,
            meta=meta,
        )


class ConflictError(AppException):
    """
    Raised when the requested operation conflicts with current state.
    """

    def __init__(
        self,
        message: str = ErrorMessages.CONFLICT_OCCURRED,
        *,
        error_code: str = ErrorCodes.CONFLICT_ERROR,
        details: Optional[List[Dict[str, Any]]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=409,
            details=details,
            meta=meta,
        )


class BusinessRuleError(AppException):
    """
    Raised when a business/domain rule blocks the requested operation.
    """

    def __init__(
        self,
        message: str = ErrorMessages.BUSINESS_RULE_VIOLATED,
        *,
        error_code: str = ErrorCodes.BUSINESS_RULE_VIOLATION,
        details: Optional[List[Dict[str, Any]]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=400,
            details=details,
            meta=meta,
        )


class UnauthorizedError(AppException):
    """
    Raised when authentication is missing or invalid.
    """

    def __init__(
        self,
        message: str = "Authentication required.",
        *,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=ErrorCodes.UNAUTHORIZED,
            status_code=401,
            meta=meta,
        )


class ForbiddenError(AppException):
    """
    Raised when access is denied despite valid authentication.
    """

    def __init__(
        self,
        message: str = "Access denied.",
        *,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=ErrorCodes.FORBIDDEN,
            status_code=403,
            meta=meta,
        )


class DeviceNotFoundError(ResourceNotFoundError):
    """
    Raised when a device does not exist.
    """

    def __init__(self, device_id: int) -> None:
        super().__init__(
            message=ErrorMessages.DEVICE_NOT_FOUND,
            error_code=ErrorCodes.DEVICE_NOT_FOUND,
            meta={"device_id": device_id},
        )


class PatientNotFoundError(ResourceNotFoundError):
    """
    Raised when a patient does not exist.
    """

    def __init__(self, patient_id: int) -> None:
        super().__init__(
            message=ErrorMessages.PATIENT_NOT_FOUND,
            error_code=ErrorCodes.PATIENT_NOT_FOUND,
            meta={"patient_id": patient_id},
        )


class DeviceAlreadyExistsError(ConflictError):
    """
    Raised when a device uniqueness constraint is violated.
    """

    def __init__(self, serial_number: str) -> None:
        super().__init__(
            message="A device with the same serial number already exists.",
            error_code="DEVICE_ALREADY_EXISTS",
            details=[
                {
                    "field": "serial_number",
                    "message": "Serial number must be unique.",
                    "code": "duplicate",
                }
            ],
            meta={"serial_number": serial_number},
        )


class DeviceAlreadyAssignedError(BusinessRuleError):
    """
    Raised when the device is already assigned to another patient.
    """

    def __init__(self, device_id: int, assigned_patient_id: Optional[int]) -> None:
        super().__init__(
            message=ErrorMessages.DEVICE_ALREADY_ASSIGNED,
            error_code=ErrorCodes.DEVICE_ALREADY_ASSIGNED,
            meta={
                "device_id": device_id,
                "assigned_patient_id": assigned_patient_id,
            },
        )


class DeviceAssignmentNotAllowedError(BusinessRuleError):
    """
    Raised when device assignment is blocked by patient/device state.
    """

    def __init__(self, patient_id: int) -> None:
        super().__init__(
            message=ErrorMessages.DEVICE_ASSIGNMENT_NOT_ALLOWED,
            error_code=ErrorCodes.DEVICE_ASSIGNMENT_NOT_ALLOWED,
            meta={"patient_id": patient_id},
        )


class HospitalNotFoundError(ResourceNotFoundError):
    """
    Raised when a hospital does not exist.
    """

    def __init__(self, hospital_id: int) -> None:
        super().__init__(
            message=ErrorMessages.HOSPITAL_NOT_FOUND,
            error_code=ErrorCodes.HOSPITAL_NOT_FOUND,
            meta={"hospital_id": hospital_id},
        )

class HospitalUnitNotFoundError(ResourceNotFoundError):
    def __init__(self, unit_id: int):
        super().__init__(f"Hospital unit with id {unit_id} not found")


class ICUNotFoundError(ResourceNotFoundError):
    """
    Raised when an ICU does not exist.
    """

    def __init__(self, icu_id: int) -> None:
        super().__init__(
            message=ErrorMessages.ICU_NOT_FOUND,
            error_code=ErrorCodes.ICU_NOT_FOUND,
            meta={"icu_id": icu_id},
        )


class BedNotFoundError(ResourceNotFoundError):
    """
    Raised when a bed does not exist.
    """

    def __init__(self, bed_id: int) -> None:
        super().__init__(
            message=ErrorMessages.BED_NOT_FOUND,
            error_code=ErrorCodes.BED_NOT_FOUND,
            meta={"bed_id": bed_id},
        )


class BedAlreadyExistsInICUError(ConflictError):
    """
    Raised when a duplicate bed number is created within the same ICU.
    """

    def __init__(self, icu_id: int, bed_number: str) -> None:
        super().__init__(
            message=ErrorMessages.BED_ALREADY_EXISTS_IN_ICU,
            error_code=ErrorCodes.BED_ALREADY_EXISTS_IN_ICU,
            details=[
                {
                    "field": "bed_number",
                    "message": "Bed number must be unique within the ICU.",
                    "code": "duplicate",
                }
            ],
            meta={
                "icu_id": icu_id,
                "bed_number": bed_number,
            },
        )