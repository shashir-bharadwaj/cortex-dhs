from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class FlowsheetRowResponse(BaseModel):
    parameter: str
    values: Dict[str, Optional[Any]] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FlowsheetResponse(BaseModel):
    patient_id: int = Field(alias="patientId")
    date: str
    hours: List[int] = Field(default_factory=list)
    rows: List[FlowsheetRowResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
