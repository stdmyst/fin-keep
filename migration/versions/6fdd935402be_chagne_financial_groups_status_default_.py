"""chagne financial_groups.status default value

Revision ID: 6fdd935402be
Revises: d4cd01e109b1
Create Date: 2025-05-25 12:18:53.553107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fdd935402be'
down_revision: Union[str, None] = 'd4cd01e109b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('ALTER TABLE financial_groups ALTER COLUMN status SET DEFAULT \'OPEN\'::financialgroupstatusesenum')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('ALTER TABLE financial_groups ALTER COLUMN status SET DEFAULT \'CLOSE\'::financialgroupstatusesenum')
