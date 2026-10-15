"""create tasks table

Revision ID: 20261015_01
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "20261015_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="todo"),
        sa.Column("priority", sa.String(length=24), nullable=False, server_default="medium"),
        sa.Column("owner", sa.String(length=80), nullable=False, server_default="Unassigned"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table("tasks")
