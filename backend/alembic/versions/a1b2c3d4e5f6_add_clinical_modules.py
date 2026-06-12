"""add clinical modules: ventilator_settings, lab_results, fluid_balance_records, medication_orders

Revision ID: a1b2c3d4e5f6
Revises: 805ca8aa1d87
Create Date: 2026-06-12 00:00:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "0010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # ventilator_settings
    # ------------------------------------------------------------------
    op.create_table(
        "ventilator_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("mode", sa.String(length=50), nullable=True),
        sa.Column("fio2", sa.Float(), nullable=True),
        sa.Column("peep", sa.Float(), nullable=True),
        sa.Column("set_rr", sa.Integer(), nullable=True),
        sa.Column("tidal_volume", sa.Float(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ventilator_settings_id"), "ventilator_settings", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_ventilator_settings_patient_id"),
        "ventilator_settings",
        ["patient_id"],
        unique=False,
    )

    # ------------------------------------------------------------------
    # lab_results
    # ------------------------------------------------------------------
    op.create_table(
        "lab_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("ph", sa.Float(), nullable=True),
        sa.Column("pao2", sa.Float(), nullable=True),
        sa.Column("paco2", sa.Float(), nullable=True),
        sa.Column("hco3", sa.Float(), nullable=True),
        sa.Column("rbs", sa.Float(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_lab_results_id"), "lab_results", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_lab_results_patient_id"), "lab_results", ["patient_id"], unique=False
    )

    # ------------------------------------------------------------------
    # fluid_balance_records
    # ------------------------------------------------------------------
    op.create_table(
        "fluid_balance_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("in_ml", sa.Float(), nullable=True),
        sa.Column("out_ml", sa.Float(), nullable=True),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_fluid_balance_records_id"),
        "fluid_balance_records",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_fluid_balance_records_patient_id"),
        "fluid_balance_records",
        ["patient_id"],
        unique=False,
    )

    # ------------------------------------------------------------------
    # medication_orders
    # ------------------------------------------------------------------
    op.create_table(
        "medication_orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("drug_name", sa.String(length=255), nullable=False),
        sa.Column("order_type", sa.String(length=50), nullable=False),
        sa.Column("dose", sa.String(length=100), nullable=True),
        sa.Column("route", sa.String(length=50), nullable=True),
        sa.Column("schedule", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("rate_ml_hr", sa.Float(), nullable=True),
        sa.Column("remaining_vol_ml", sa.Float(), nullable=True),
        sa.Column("est_end_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_medication_orders_id"), "medication_orders", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_medication_orders_patient_id"),
        "medication_orders",
        ["patient_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_medication_orders_patient_id"), table_name="medication_orders")
    op.drop_index(op.f("ix_medication_orders_id"), table_name="medication_orders")
    op.drop_table("medication_orders")

    op.drop_index(
        op.f("ix_fluid_balance_records_patient_id"),
        table_name="fluid_balance_records",
    )
    op.drop_index(
        op.f("ix_fluid_balance_records_id"), table_name="fluid_balance_records"
    )
    op.drop_table("fluid_balance_records")

    op.drop_index(op.f("ix_lab_results_patient_id"), table_name="lab_results")
    op.drop_index(op.f("ix_lab_results_id"), table_name="lab_results")
    op.drop_table("lab_results")

    op.drop_index(
        op.f("ix_ventilator_settings_patient_id"), table_name="ventilator_settings"
    )
    op.drop_index(op.f("ix_ventilator_settings_id"), table_name="ventilator_settings")
    op.drop_table("ventilator_settings")
