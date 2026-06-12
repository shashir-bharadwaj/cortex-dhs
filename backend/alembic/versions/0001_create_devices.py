"""create devices module

Revision ID: 0001
Revises:
Create Date: 2026-04-15 18:17:29.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "device_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("company", sa.String(), nullable=True),
        sa.Column("output_spec", sa.String(), nullable=True),
        sa.Column("adapter_name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_device_types_id"), "device_types", ["id"], unique=False)

    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("serial_number", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("last_sync", sa.DateTime(), nullable=True),
        sa.Column("error", sa.String(), nullable=True),
        sa.Column("location", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_devices_id"), "devices", ["id"], unique=False)
    op.create_index(op.f("ix_devices_serial_number"), "devices", ["serial_number"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_devices_serial_number"), table_name="devices")
    op.drop_index(op.f("ix_devices_id"), table_name="devices")
    op.drop_table("devices")

    op.drop_index(op.f("ix_device_types_id"), table_name="device_types")
    op.drop_table("device_types")
