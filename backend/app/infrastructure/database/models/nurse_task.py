from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.domain.enums.task import TaskStatus


class NurseTaskModel(Base):
    __tablename__ = "nurse_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"), nullable=False, index=True
    )

    patient_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bed_label: Mapped[str] = mapped_column(String(50), nullable=False)

    assigned_to_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    due_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    status: Mapped[TaskStatus] = mapped_column(
        Enum(
            TaskStatus,
            values_callable=lambda e: [i.value for i in e],
            name="taskstatus",
        ),
        nullable=False,
        default=TaskStatus.PENDING,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    patient = relationship("PatientModel")
    assigned_to = relationship("UserModel", foreign_keys=[assigned_to_id])
