"""create patient assignments module (staff and device assignments)

Revision ID: 0010
Revises: 0009
Create Date: 2026-04-15 18:17:29.900000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0010"
down_revision: Union[str, None] = "0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "patient_staff_assignments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("assignment_type", sa.String(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(), nullable=False),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_patient_staff_assignments_id"),
        "patient_staff_assignments",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_patient_staff_assignments_patient_id"),
        "patient_staff_assignments",
        ["patient_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_patient_staff_assignments_user_id"),
        "patient_staff_assignments",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_patient_staff_assignments_is_active"),
        "patient_staff_assignments",
        ["is_active"],
        unique=False,
    )

    op.create_table(
        "patient_devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(), nullable=True),
        sa.Column("removed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"]),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_patient_devices_id"), "patient_devices", ["id"], unique=False)
    op.create_index(
        op.f("ix_patient_devices_patient_id"), "patient_devices", ["patient_id"], unique=False
    )
    op.create_index(
        op.f("ix_patient_devices_device_id"), "patient_devices", ["device_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_patient_devices_device_id"), table_name="patient_devices")
    op.drop_index(op.f("ix_patient_devices_patient_id"), table_name="patient_devices")
    op.drop_index(op.f("ix_patient_devices_id"), table_name="patient_devices")
    op.drop_table("patient_devices")

    op.drop_index(
        op.f("ix_patient_staff_assignments_is_active"),
        table_name="patient_staff_assignments",
    )
    op.drop_index(
        op.f("ix_patient_staff_assignments_user_id"),
        table_name="patient_staff_assignments",
    )
    op.drop_index(
        op.f("ix_patient_staff_assignments_patient_id"),
        table_name="patient_staff_assignments",
    )
    op.drop_index(
        op.f("ix_patient_staff_assignments_id"),
        table_name="patient_staff_assignments",
    )
    op.drop_table("patient_staff_assignments")
