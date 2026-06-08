from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class RoleModel(Base):
    """
    SQLAlchemy model for system roles.
    """

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    users = relationship(
        "UserModel",
        back_populates="role",
    )

    role_permissions = relationship(
        "RolePermissionModel",
        back_populates="role",
        cascade="all, delete-orphan",
    )