"""create audit_logs table

Revision ID: 5c44611eb298
Revises: 0011
Create Date: 2026-07-10 09:54:47.440377

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "5c44611eb298"
down_revision: Union[str, None] = "0011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create audit_logs table.
    """
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("user", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("module", sa.String(), nullable=False),
        sa.Column("ip_address", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_audit_logs_id"),
        "audit_logs",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_audit_logs_timestamp"),
        "audit_logs",
        ["timestamp"],
        unique=False,
    )


def downgrade() -> None:
    """
    Drop audit_logs table.
    """
    op.drop_index(
        op.f("ix_audit_logs_timestamp"),
        table_name="audit_logs",
    )

    op.drop_index(
        op.f("ix_audit_logs_id"),
        table_name="audit_logs",
    )

    op.drop_table("audit_logs")