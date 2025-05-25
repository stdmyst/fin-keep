"""Add TRANSEFER fin type to FinancialTypesEnum (renamed)

Revision ID: d4cd01e109b1
Revises: d9d563b83813
Create Date: 2025-05-24 21:40:10.253611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd4cd01e109b1'
down_revision: Union[str, None] = 'd9d563b83813'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('ALTER TYPE financialgrouptypesenum RENAME TO financialtypesenum')
    op.execute('ALTER TYPE financialtypesenum ADD VALUE IF NOT EXISTS \'TRANSFER\'')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('CREATE TYPE financialgrouptypesenum AS ENUM (\'GOAL\', \'CREDIT\');')
    op.execute('ALTER TABLE transactions ALTER COLUMN target_type TYPE financialgrouptypesenum USING (target_type::text::financialgrouptypesenum)')
    op.execute('DROP TYPE IF EXISTS financialtypesenum CASCADE;')
