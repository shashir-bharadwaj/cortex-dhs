"""create patients module

Revision ID: 0006
Revises: 0005
Create Date: 2026-04-15 18:17:29.500000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0006"
down_revision: Union[str, None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mrn", sa.String(length=100), nullable=False),
        sa.Column("cr_number", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("contact_number", sa.String(length=20), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column(
            "gender",
            sa.Enum("MALE", "FEMALE", "OTHER", name="gender"),
            nullable=False,
        ),
        sa.Column("weight", sa.Float(), nullable=True),
        sa.Column("height", sa.Float(), nullable=True),
        sa.Column("blood_group", sa.String(), nullable=True),
        sa.Column("bed_id", sa.Integer(), nullable=True),
        sa.Column("diagnosis", sa.String(), nullable=True),
        sa.Column("doctor", sa.String(), nullable=True),
        sa.Column("admission_time", sa.DateTime(), nullable=False),
        sa.Column("hospital_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("history", sa.JSON(), nullable=True),
        sa.Column("comorbidities", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["bed_id"], ["bed_masters.id"]),
        sa.ForeignKeyConstraint(["hospital_id"], ["hospitals.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_patients_id"), "patients", ["id"], unique=False)
    op.create_index(op.f("ix_patients_bed_id"), "patients", ["bed_id"], unique=False)
    op.create_index(op.f("ix_patients_hospital_id"), "patients", ["hospital_id"], unique=False)
    op.create_index(op.f("ix_patients_mrn"), "patients", ["mrn"], unique=False)
    op.create_index(op.f("ix_patients_cr_number"), "patients", ["cr_number"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_patients_cr_number"), table_name="patients")
    op.drop_index(op.f("ix_patients_mrn"), table_name="patients")
    op.drop_index(op.f("ix_patients_hospital_id"), table_name="patients")
    op.drop_index(op.f("ix_patients_bed_id"), table_name="patients")
    op.drop_index(op.f("ix_patients_id"), table_name="patients")
    op.drop_table("patients")
    op.execute("DROP TYPE IF EXISTS gender")
