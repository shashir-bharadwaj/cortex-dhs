from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: int
    time: str
    user: str
    role: str
    action: str
    module: str
    ip: str

    model_config = ConfigDict(from_attributes=True)
