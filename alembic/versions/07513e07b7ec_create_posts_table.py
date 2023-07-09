"""create posts table

Revision ID: 07513e07b7ec
Revises: 
Create Date: 2023-07-09 22:34:18.175223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07513e07b7ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
