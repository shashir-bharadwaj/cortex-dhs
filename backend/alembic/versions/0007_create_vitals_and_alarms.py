"""create vitals and alarms modules

Revision ID: 0007
Revises: 0006
Create Date: 2026-04-15 18:17:29.600000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "vitals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("hr", sa.Float(), nullable=True),
        sa.Column("bp_sys", sa.Float(), nullable=True),
        sa.Column("bp_dia", sa.Float(), nullable=True),
        sa.Column("spo2", sa.Float(), nullable=True),
        sa.Column("temp", sa.Float(), nullable=True),
        sa.Column("rr", sa.Float(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vitals_id"), "vitals", ["id"], unique=False)
    op.create_index(op.f("ix_vitals_patient_id"), "vitals", ["patient_id"], unique=False)

    op.create_table(
        "latest_patient_vitals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("bed_id", sa.Integer(), nullable=True),
        sa.Column("device_id", sa.Integer(), nullable=True),
        sa.Column("hr", sa.Float(), nullable=True),
        sa.Column("bp_sys", sa.Float(), nullable=True),
        sa.Column("bp_dia", sa.Float(), nullable=True),
        sa.Column("spo2", sa.Float(), nullable=True),
        sa.Column("temp", sa.Float(), nullable=True),
        sa.Column("rr", sa.Float(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.ForeignKeyConstraint(["bed_id"], ["bed_masters.id"]),
        sa.ForeignKeyConstraint(["device_id"], ["device_masters.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("patient_id", name="uq_latest_patient_vitals_patient_id"),
    )
    op.create_index(
        op.f("ix_latest_patient_vitals_id"), "latest_patient_vitals", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_latest_patient_vitals_patient_id"),
        "latest_patient_vitals",
        ["patient_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_latest_patient_vitals_bed_id"),
        "latest_patient_vitals",
        ["bed_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_latest_patient_vitals_device_id"),
        "latest_patient_vitals",
        ["device_id"],
        unique=False,
    )

    op.create_table(
        "alarms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("patient_name", sa.String(), nullable=False),
        sa.Column("bed_id", sa.String(), nullable=False),
        sa.Column("device", sa.String(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("severity", sa.String(), nullable=False),
        sa.Column("acknowledged", sa.Boolean(), nullable=False),
        sa.Column("silenced", sa.Boolean(), nullable=False),
        sa.Column("escalated", sa.Boolean(), nullable=False),
        sa.Column("acknowledged_by", sa.String(), nullable=True),
        sa.Column("silenced_by", sa.String(), nullable=True),
        sa.Column("silence_until", sa.DateTime(), nullable=True),
        sa.Column("escalated_by", sa.String(), nullable=True),
        sa.Column("escalate_to", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_alarms_id"), "alarms", ["id"], unique=False)
    op.create_index(op.f("ix_alarms_patient_id"), "alarms", ["patient_id"], unique=False)
    op.create_index(op.f("ix_alarms_severity"), "alarms", ["severity"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_alarms_severity"), table_name="alarms")
    op.drop_index(op.f("ix_alarms_patient_id"), table_name="alarms")
    op.drop_index(op.f("ix_alarms_id"), table_name="alarms")
    op.drop_table("alarms")

    op.drop_index(op.f("ix_latest_patient_vitals_device_id"), table_name="latest_patient_vitals")
    op.drop_index(op.f("ix_latest_patient_vitals_bed_id"), table_name="latest_patient_vitals")
    op.drop_index(op.f("ix_latest_patient_vitals_patient_id"), table_name="latest_patient_vitals")
    op.drop_index(op.f("ix_latest_patient_vitals_id"), table_name="latest_patient_vitals")
    op.drop_table("latest_patient_vitals")

    op.drop_index(op.f("ix_vitals_patient_id"), table_name="vitals")
    op.drop_index(op.f("ix_vitals_id"), table_name="vitals")
    op.drop_table("vitals")
