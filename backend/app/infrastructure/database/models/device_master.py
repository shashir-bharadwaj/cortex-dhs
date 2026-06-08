from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class DeviceMasterModel(Base):
    """
    SQLAlchemy model for device master records.

    Relationship:
    -------------
    A device can optionally be mapped to one bed.
    """

    __tablename__ = "device_masters"

    id = Column(Integer, primary_key=True, index=True)

    device_type = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    model = Column(String, nullable=False)

    serial = Column(String, nullable=False, unique=True, index=True)

    bed_id = Column(
        Integer,
        ForeignKey("bed_masters.id"),
        nullable=True,
        index=True,
    )

    ip_address = Column(String, nullable=False)
    status = Column(String, nullable=False, default="ACTIVE")

    bed = relationship(
        "BedMasterModel",
        back_populates="devices",
    )