"""create nurse_tasks table

Revision ID: 0011
Revises: a1b2c3d4e5f6
Create Date: 2026-06-16 00:00:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0011"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "nurse_tasks",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patients.id"), nullable=False, index=True),
        sa.Column("patient_name", sa.String(255), nullable=False),
        sa.Column("bed_label", sa.String(50), nullable=False),
        sa.Column("assigned_to_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("due_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "status",
            sa.Enum("pending", "in_progress", "completed", name="taskstatus"),
            nullable=False,
            server_default="pending",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_nurse_tasks_status", "nurse_tasks", ["status"])


def downgrade() -> None:
    op.drop_table("nurse_tasks")
    op.execute("DROP TYPE IF EXISTS taskstatus")
