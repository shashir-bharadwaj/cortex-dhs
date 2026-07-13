from sqlalchemy import Column, DateTime, Integer, String

from app.db.database import Base


class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)

    user = Column(String, nullable=False)
    role = Column(String, nullable=False)

    action = Column(String, nullable=False)
    module = Column(String, nullable=False)

    ip_address = Column(String, nullable=False)