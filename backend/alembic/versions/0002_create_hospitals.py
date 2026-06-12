"""create hospitals module

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-15 18:17:29.100000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hospitals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=True),
        sa.Column("address", sa.String(length=500), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("contact_number", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_hospitals_id"), "hospitals", ["id"], unique=False)

    op.create_table(
        "hospital_units",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hospital_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["hospital_id"], ["hospitals.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hospital_id", "name", name="uq_hospital_units_hospital_id_name"),
    )
    op.create_index(
        op.f("ix_hospital_units_hospital_id"), "hospital_units", ["hospital_id"], unique=False
    )
    op.create_index(op.f("ix_hospital_units_id"), "hospital_units", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_hospital_units_id"), table_name="hospital_units")
    op.drop_index(op.f("ix_hospital_units_hospital_id"), table_name="hospital_units")
    op.drop_table("hospital_units")

    op.drop_index(op.f("ix_hospitals_id"), table_name="hospitals")
    op.drop_table("hospitals")
