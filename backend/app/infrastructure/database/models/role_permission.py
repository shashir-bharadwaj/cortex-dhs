from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class RolePermissionModel(Base):
    """
    SQLAlchemy model for role-permission mappings.
    """

    __tablename__ = "role_permissions"

    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "permission_id",
            name="uq_role_permission",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    )

    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE"),
        nullable=False,
    )

    role = relationship(
        "RoleModel",
        back_populates="role_permissions",
    )

    permission = relationship(
        "PermissionModel",
        back_populates="role_permissions",
    )