from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class ICUUnitMasterModel(Base):
    """
    SQLAlchemy model for ICU units.

    Relationship:
    - One ICU unit can have multiple beds.
    """

    __tablename__ = "icu_unit_masters"

    id = Column(Integer, primary_key=True, index=True)

    icu_name = Column(String, nullable=False, unique=True, index=True)
    type = Column(String, nullable=False)
    department = Column(String, nullable=False)

    # Kept for backward compatibility for now.
    # Actual bed/device mapping should come from relationships.
    beds = Column(Integer, nullable=False, default=0)
    devices = Column(String, nullable=True)

    gateway = Column(String, nullable=True)
    status = Column(String, nullable=False, default="ACTIVE")

    beds_list = relationship(
        "BedMasterModel",
        back_populates="icu_unit",
        cascade="all, delete-orphan",
    )