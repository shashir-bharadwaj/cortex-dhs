from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class UserModel(Base):
    """
    SQLAlchemy model for application users.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
        index=True,
    )

    hospital_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    unit_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    shift: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    role = relationship(
        "RoleModel",
        back_populates="users",
    )