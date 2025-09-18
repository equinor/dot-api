"""add project role tabela and add is default

Revision ID: 589643041c80
Revises: ee08f39e47aa, 355ec823911a
Create Date: 2025-09-09 13:00:00.299541

"""
from typing import Sequence, Union



# revision identifiers, used by Alembic.
revision: str = '589643041c80'
down_revision: Union[str, tuple[str, ...], None] = ('ee08f39e47aa', '355ec823911a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
