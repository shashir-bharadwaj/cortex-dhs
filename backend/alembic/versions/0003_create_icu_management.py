"""create icu management module (icu units, beds, device masters)

Revision ID: 0003
Revises: 0002
Create Date: 2026-04-15 18:17:29.200000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "icu_unit_masters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("icu_name", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("department", sa.String(), nullable=False),
        sa.Column("beds", sa.Integer(), nullable=False),
        sa.Column("devices", sa.String(), nullable=True),
        sa.Column("gateway", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_icu_unit_masters_id"), "icu_unit_masters", ["id"], unique=False)
    op.create_index(
        op.f("ix_icu_unit_masters_icu_name"), "icu_unit_masters", ["icu_name"], unique=True
    )

    op.create_table(
        "bed_masters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bed_id", sa.String(), nullable=False),
        sa.Column("icu_unit_id", sa.Integer(), nullable=False),
        sa.Column("bed_type", sa.String(), nullable=False),
        sa.Column("department", sa.String(), nullable=False),
        sa.Column("ward", sa.String(), nullable=False),
        sa.Column("floor", sa.String(), nullable=False),
        sa.Column("room", sa.String(), nullable=False),
        sa.Column("cleaning_status", sa.String(), nullable=False),
        sa.Column("maintenance_status", sa.String(), nullable=False),
        sa.Column("operational_status", sa.String(), nullable=False),
        sa.Column("last_sanitized", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["icu_unit_id"], ["icu_unit_masters.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_bed_masters_id"), "bed_masters", ["id"], unique=False)
    op.create_index(op.f("ix_bed_masters_bed_id"), "bed_masters", ["bed_id"], unique=True)
    op.create_index(
        op.f("ix_bed_masters_icu_unit_id"), "bed_masters", ["icu_unit_id"], unique=False
    )

    op.create_table(
        "device_masters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("device_type", sa.String(), nullable=False),
        sa.Column("manufacturer", sa.String(), nullable=False),
        sa.Column("model", sa.String(), nullable=False),
        sa.Column("serial", sa.String(), nullable=False),
        sa.Column("bed_id", sa.Integer(), nullable=True),
        sa.Column("ip_address", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["bed_id"], ["bed_masters.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_device_masters_id"), "device_masters", ["id"], unique=False)
    op.create_index(op.f("ix_device_masters_serial"), "device_masters", ["serial"], unique=True)
    op.create_index(
        op.f("ix_device_masters_bed_id"), "device_masters", ["bed_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_device_masters_bed_id"), table_name="device_masters")
    op.drop_index(op.f("ix_device_masters_serial"), table_name="device_masters")
    op.drop_index(op.f("ix_device_masters_id"), table_name="device_masters")
    op.drop_table("device_masters")

    op.drop_index(op.f("ix_bed_masters_icu_unit_id"), table_name="bed_masters")
    op.drop_index(op.f("ix_bed_masters_bed_id"), table_name="bed_masters")
    op.drop_index(op.f("ix_bed_masters_id"), table_name="bed_masters")
    op.drop_table("bed_masters")

    op.drop_index(op.f("ix_icu_unit_masters_icu_name"), table_name="icu_unit_masters")
    op.drop_index(op.f("ix_icu_unit_masters_id"), table_name="icu_unit_masters")
    op.drop_table("icu_unit_masters")
