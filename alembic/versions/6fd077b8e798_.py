"""empty message

Revision ID: 6fd077b8e798
Revises: 84ee713797e0, c9f840341a96
Create Date: 2025-11-13 12:47:38.035677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fd077b8e798'
down_revision: Union[str, None] = ('84ee713797e0', 'c9f840341a96')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
