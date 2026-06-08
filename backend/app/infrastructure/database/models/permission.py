from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class PermissionModel(Base):
    """
    SQLAlchemy model for RBAC permissions.
    """

    __tablename__ = "permissions"

    __table_args__ = (
        UniqueConstraint(
            "module",
            "action",
            name="uq_permission_module_action",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    module: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    role_permissions = relationship(
        "RolePermissionModel",
        back_populates="permission",
        cascade="all, delete-orphan",
    )