from pydantic import BaseModel, ConfigDict, Field


class ReportCardResponse(BaseModel):
    title: str
    desc: str

    model_config = ConfigDict()


class IcuDataResponse(BaseModel):
    name: str
    value: int

    model_config = ConfigDict()


class AlertDataResponse(BaseModel):
    time: str
    critical: int
    warning: int
    info: int

    model_config = ConfigDict()


class ReportsResponse(BaseModel):
    report_cards: list[ReportCardResponse] = Field(alias="reportCards")
    icu_data: list[IcuDataResponse] = Field(alias="icuData")
    alert_data: list[AlertDataResponse] = Field(alias="alertData")

    model_config = ConfigDict(populate_by_name=True)
