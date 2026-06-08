from sqlalchemy import Column, Integer, String

from app.db.database import Base


class DeviceType(Base):
    """
    SQLAlchemy model for device types.
    """

    __tablename__ = "device_types"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=True)
    company = Column(String, nullable=True)
    output_spec = Column(String, nullable=True)
    adapter_name = Column(String, nullable=True)