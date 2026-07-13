from pydantic import BaseModel, ConfigDict, Field


class AdminDashboardStatsResponse(BaseModel):
    hospitals: int
    icu_units: int = Field(alias="icuUnits")
    beds: int
    connected: int
    offline: int
    patients: int
    critical: int

    model_config = ConfigDict(populate_by_name=True)


class AdminDashboardConnectivityPointResponse(BaseModel):
    time: str
    online: int
    offline: int


class AdminDashboardAlertPointResponse(BaseModel):
    time: str
    critical: int
    warning: int
    info: int


class AdminDashboardLiveAlertResponse(BaseModel):
    bed: str
    type: str
    message: str
    time: str


class AdminDashboardOverviewResponse(BaseModel):
    stats: AdminDashboardStatsResponse
    connectivity_trend: list[AdminDashboardConnectivityPointResponse] = Field(alias="connectivityTrend")
    alerts_data: list[AdminDashboardAlertPointResponse] = Field(alias="alertsData")
    live_alerts: list[AdminDashboardLiveAlertResponse] = Field(alias="liveAlerts")

    model_config = ConfigDict(populate_by_name=True)
