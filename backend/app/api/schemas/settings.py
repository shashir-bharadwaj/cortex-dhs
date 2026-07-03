from pydantic import BaseModel, ConfigDict, Field


class SettingsPayload(BaseModel):
    hospital_name: str = Field(alias="hospitalName")
    admin_email: str = Field(alias="adminEmail")
    settings: dict[str, bool]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SettingsResponse(BaseModel):
    hospital_name: str = Field(alias="hospitalName")
    admin_email: str = Field(alias="adminEmail")
    settings: dict[str, bool]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
