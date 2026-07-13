from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AuditLog:
    id: Optional[int]
    timestamp: datetime
    user: str
    role: str
    action: str
    module: str
    ip_address: str