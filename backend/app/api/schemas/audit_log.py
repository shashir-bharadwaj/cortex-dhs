from datetime import datetime

from pydantic import BaseModel


class AuditLogCreateRequest(BaseModel):
    timestamp: datetime
    user: str
    role: str
    action: str
    module: str
    ip_address: str


class AuditLogUpdateRequest(BaseModel):
    timestamp: datetime
    user: str
    role: str
    action: str
    module: str
    ip_address: str


class AuditLogResponse(BaseModel):
    id: int
    timestamp: datetime
    user: str
    role: str
    action: str
    module: str
    ip_address: str

    class Config:
        from_attributes = True