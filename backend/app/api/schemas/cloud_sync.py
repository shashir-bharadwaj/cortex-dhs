from pydantic import BaseModel, ConfigDict, Field


class HospitalSyncResponse(BaseModel):
    id: int
    name: str
    city: str
    status: str
    last_sync: str = Field(..., alias="lastSync")
    data: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CloudSummaryResponse(BaseModel):
    last_sync: str = Field(..., alias="lastSync")
    data_sent: str = Field(..., alias="dataSent")
    errors: int
    hospitals: int

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CloudSyncResponse(BaseModel):
    summary: CloudSummaryResponse
    hospitals: list[HospitalSyncResponse]

    model_config = ConfigDict(from_attributes=True)


class CloudSyncTriggerResponse(BaseModel):
    started: bool
    message: str

    model_config = ConfigDict(from_attributes=True)
