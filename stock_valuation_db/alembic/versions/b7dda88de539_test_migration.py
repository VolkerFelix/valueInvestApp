"""Test migration

Revision ID: b7dda88de539
Revises: 
Create Date: 2024-02-24 09:17:20.974744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7dda88de539'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("name", sa.String))


def downgrade() -> None:
    pass
