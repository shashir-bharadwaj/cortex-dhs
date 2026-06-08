from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.enums.auth import ShiftType


class UserCreateRequest(BaseModel):
    """
    Request schema for creating a user from admin console.
    """

    first_name: str = Field(..., alias="firstName", min_length=1)
    last_name: str = Field(..., alias="lastName", min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role_id: int = Field(..., alias="roleId", gt=0)

    hospital_id: int | None = Field(default=None, alias="hospitalId")
    unit_id: int | None = Field(default=None, alias="unitId")
    shift: ShiftType | None = None

    model_config = ConfigDict(populate_by_name=True)


class UserUpdateRequest(BaseModel):
    """
    Request schema for updating user details from admin console.
    """

    first_name: str = Field(..., alias="firstName", min_length=1)
    last_name: str = Field(..., alias="lastName", min_length=1)
    email: EmailStr
    role_id: int = Field(..., alias="roleId", gt=0)

    hospital_id: int | None = Field(default=None, alias="hospitalId")
    unit_id: int | None = Field(default=None, alias="unitId")
    shift: ShiftType | None = None
    is_active: bool = Field(..., alias="isActive")

    model_config = ConfigDict(populate_by_name=True)


class UserStatusUpdateRequest(BaseModel):
    """
    Request schema for activating/deactivating a user.
    """

    is_active: bool = Field(..., alias="isActive")

    model_config = ConfigDict(populate_by_name=True)


class UserPasswordResetRequest(BaseModel):
    """
    Request schema for resetting a user's password.
    """

    password: str = Field(..., min_length=6)


class UserRoleUpdateRequest(BaseModel):
    """
    Request schema for changing a user's role.
    """

    role_id: int = Field(..., alias="roleId", gt=0)

    model_config = ConfigDict(populate_by_name=True)


class ModulePermissionsUpdateRequest(BaseModel):
    """
    Permission update payload for a single module.
    """

    module: str
    allowed_actions: list[str] = Field(
        default_factory=list,
        alias="allowedActions",
    )

    model_config = ConfigDict(populate_by_name=True)


class RolePermissionsUpdateRequest(BaseModel):
    """
    Request schema for replacing permissions assigned to a role.

    Frontend sends permissions grouped by module with allowed actions.
    """

    permissions: list[ModulePermissionsUpdateRequest] = Field(
        default_factory=list,
    )

    model_config = ConfigDict(populate_by_name=True)


class UserResponse(BaseModel):
    """
    Admin user response schema.
    """

    id: int
    user_id: str = Field(..., alias="userId")

    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    email: str

    role_id: int = Field(..., alias="roleId")
    role: str | None = None

    hospital_id: int | None = Field(default=None, alias="hospitalId")
    unit_id: int | None = Field(default=None, alias="unitId")

    shift: ShiftType | None = None
    is_active: bool = Field(..., alias="isActive")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ModulePermissionMatrixResponse(BaseModel):
    """
    Permission summary for a single module under a role.
    """

    module: str
    module_name: str = Field(..., alias="moduleName")
    allowed_actions: list[str] = Field(
        default_factory=list,
        alias="allowedActions",
    )

    model_config = ConfigDict(populate_by_name=True)


class RolePermissionMatrixResponse(BaseModel):
    """
    Frontend-friendly permission matrix for one role.
    """

    role_id: int = Field(..., alias="roleId")
    role: str
    permissions: list[ModulePermissionMatrixResponse]

    model_config = ConfigDict(populate_by_name=True)


class RolePermissionMatrixListResponse(BaseModel):
    """
    Wrapper response for role permission matrix list.

    Keeps the API response self-descriptive and allows metadata
    to be added later without changing the top-level response shape.
    """

    role_permissions: list[RolePermissionMatrixResponse] = Field(
        default_factory=list,
        alias="rolePermissions",
    )

    model_config = ConfigDict(populate_by_name=True)