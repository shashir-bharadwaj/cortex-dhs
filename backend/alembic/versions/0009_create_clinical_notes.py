"""create clinical notes module

Revision ID: 0009
Revises: 0008
Create Date: 2026-04-15 18:17:29.800000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0009"
down_revision: Union[str, None] = "0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "clinical_notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("author_name", sa.String(length=255), nullable=False),
        sa.Column(
            "note_type",
            sa.Enum(
                "progress",
                "nursing",
                "order",
                "handover",
                name="clinicalnotetype",
            ),
            nullable=False,
        ),
        sa.Column("note_text", sa.Text(), nullable=False),
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
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_clinical_notes_id"), "clinical_notes", ["id"], unique=False)
    op.create_index(
        op.f("ix_clinical_notes_patient_id"), "clinical_notes", ["patient_id"], unique=False
    )
    op.create_index(
        op.f("ix_clinical_notes_author_id"), "clinical_notes", ["author_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_clinical_notes_author_id"), table_name="clinical_notes")
    op.drop_index(op.f("ix_clinical_notes_patient_id"), table_name="clinical_notes")
    op.drop_index(op.f("ix_clinical_notes_id"), table_name="clinical_notes")
    op.drop_table("clinical_notes")
    op.execute("DROP TYPE IF EXISTS clinicalnotetype")
