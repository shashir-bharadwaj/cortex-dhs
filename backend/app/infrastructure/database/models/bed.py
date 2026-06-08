from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class BedMasterModel(Base):
    """
    SQLAlchemy model for beds.

    Relationship:
    - Many beds belong to one ICU unit.
    - One bed can have multiple devices.
    """

    __tablename__ = "bed_masters"

    id = Column(Integer, primary_key=True, index=True)

    bed_id = Column(String, nullable=False, unique=True, index=True)

    icu_unit_id = Column(
        Integer,
        ForeignKey("icu_unit_masters.id"),
        nullable=False,
        index=True,
    )

    bed_type = Column(String, nullable=False)
    department = Column(String, nullable=False)
    ward = Column(String, nullable=False)
    floor = Column(String, nullable=False)
    room = Column(String, nullable=False)

    cleaning_status = Column(String, nullable=False)
    maintenance_status = Column(String, nullable=False)
    operational_status = Column(String, nullable=False)

    last_sanitized = Column(DateTime, nullable=True)

    icu_unit = relationship(
        "ICUUnitMasterModel",
        back_populates="beds_list",
    )

    devices = relationship(
        "DeviceMasterModel",
        back_populates="bed",
    )