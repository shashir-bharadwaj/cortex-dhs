from pydantic import BaseModel, ConfigDict, Field


class ConnectivityDeviceResponse(BaseModel):
    id: str
    type: str
    bed: str
    status: str
    last_sync: str = Field(alias="lastSync")
    ip: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ConnectivitySummaryResponse(BaseModel):
    online: int
    offline: int
    data_rate: str = Field(alias="dataRate")
    latency: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ConnectivityTimelineResponse(BaseModel):
    time: str
    online: int
    offline: int

    model_config = ConfigDict(from_attributes=True)


class ConnectivityResponse(BaseModel):
    summary: ConnectivitySummaryResponse
    timeline: list[ConnectivityTimelineResponse]
    devices: list[ConnectivityDeviceResponse]

    model_config = ConfigDict(from_attributes=True)
