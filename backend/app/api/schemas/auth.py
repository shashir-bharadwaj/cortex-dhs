"""
Pydantic schemas for authentication-related requests and responses.
"""

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums.auth import ShiftType


# =========================================================
# Login Request
# =========================================================

class LoginRequest(BaseModel):
    """
    Login request payload.
    """

    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


# =========================================================
# Authenticated User Response
# =========================================================

class AuthUserResponse(BaseModel):
    """
    Authenticated user payload returned in auth responses.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    userId: str

    firstName: str
    lastName: str

    email: str

    roleId: int

    hospitalId: int | None
    unitId: int | None

    shift: ShiftType | None

    isActive: bool


# =========================================================
# Login Response
# =========================================================

class LoginResponse(BaseModel):
    """
    Login response containing JWT token and authenticated user.
    """

    token: str
    user: AuthUserResponse


# =========================================================
# Current User Response
# =========================================================

class CurrentUserResponse(BaseModel):
    """
    Response schema for current authenticated user.

    Includes permission matrix used by frontend to render
    module-level and action-level access.
    """

    id: int

    userId: str

    firstName: str
    lastName: str

    email: str

    roleId: int

    hospitalId: int | None
    unitId: int | None

    shift: ShiftType | None

    isActive: bool

    permissions: dict[str, list[str]] = {}


# =========================================================
# Update Shift Request
# =========================================================

class UpdateShiftRequest(BaseModel):
    """
    Request payload for updating shift details.
    """

    shift: ShiftType

    unitId: int = Field(..., gt=0)


# =========================================================
# Update Shift Response
# =========================================================

class UpdateShiftResponse(BaseModel):
    """
    Response payload after updating shift details.
    """

    shift: ShiftType

    unitId: int