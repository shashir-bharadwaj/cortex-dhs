"""create timeline module

Revision ID: 0008
Revises: 0007
Create Date: 2026-04-15 18:17:29.700000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0008"
down_revision: Union[str, None] = "0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "timeline_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "DEVICE_ASSIGNED",
                "DEVICE_REMOVED",
                "STATUS_CHANGED",
                "NOTE_ADDED",
                name="timelineeventtype",
            ),
            nullable=False,
        ),
        sa.Column("event", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_timeline_events_id"), "timeline_events", ["id"], unique=False)
    op.create_index(
        op.f("ix_timeline_events_patient_id"), "timeline_events", ["patient_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_timeline_events_patient_id"), table_name="timeline_events")
    op.drop_index(op.f("ix_timeline_events_id"), table_name="timeline_events")
    op.drop_table("timeline_events")
    op.execute("DROP TYPE IF EXISTS timelineeventtype")
