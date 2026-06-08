from pydantic import BaseModel, ConfigDict, Field


class ModulePermissionsRequest(BaseModel):
    """
    Permission payload for one module.

    Example:
    {
        "module": "PATIENTS",
        "allowedActions": ["VIEW", "CREATE"]
    }
    """

    module: str
    allowed_actions: list[str] = Field(
        default_factory=list,
        alias="allowedActions",
    )

    model_config = ConfigDict(populate_by_name=True)


class RoleCreateRequest(BaseModel):
    """
    Request schema for creating a role.

    Uses frontend-friendly module/action permissions instead of raw
    permission IDs.
    """

    name: str = Field(..., min_length=1)
    description: str | None = None

    permissions: list[ModulePermissionsRequest] = Field(
        default_factory=list,
    )

    model_config = ConfigDict(populate_by_name=True)


class RoleResponse(BaseModel):
    """
    Response schema for roles.
    """

    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class PermissionResponse(BaseModel):
    """
    Raw permission response schema.

    Keep this available for internal/debug/admin catalog APIs if needed.
    """

    id: int
    module: str
    action: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)