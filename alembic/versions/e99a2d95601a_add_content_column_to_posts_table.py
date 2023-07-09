"""add content column to posts table

Revision ID: e99a2d95601a
Revises: 07513e07b7ec
Create Date: 2023-07-09 22:46:57.742964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e99a2d95601a'
down_revision = '07513e07b7ec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
