"""
Central registry of reusable user-facing error messages.

Use this file to keep business messages consistent across routes, use cases,
and future modules. It makes later text changes much easier.
"""


class ErrorMessages:
    """
    Reusable error message constants.
    """

    INTERNAL_SERVER_ERROR = "An unexpected error occurred."
    REQUEST_VALIDATION_FAILED = "Request validation failed."
    VALIDATION_FAILED = "Validation failed."

    RESOURCE_NOT_FOUND = "Requested resource was not found."
    CONFLICT_OCCURRED = "The request conflicts with the current resource state."
    BUSINESS_RULE_VIOLATED = "The requested operation violates a business rule."

    DEVICE_NOT_FOUND = "Device not found."
    PATIENT_NOT_FOUND = "Patient not found."
    DEVICE_ALREADY_EXISTS = "A device with the same serial number already exists."
    DEVICE_ALREADY_ASSIGNED = "Device is already assigned to another patient."
    DEVICE_ASSIGNMENT_NOT_ALLOWED = "Device assignment is not allowed for this patient."

    HOSPITAL_NOT_FOUND = "Hospital not found."
    ICU_NOT_FOUND = "ICU not found."
    BED_NOT_FOUND = "Bed not found."
    BED_ALREADY_EXISTS_IN_ICU = "A bed with the same bed number already exists in this ICU."