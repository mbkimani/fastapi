"""add the rest of the columns on posts table

Revision ID: ffadea8b379b
Revises: 7df43f56f3b1
Create Date: 2021-11-24 14:35:07.909536

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = 'ffadea8b379b'
down_revision = '7df43f56f3b1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='True', nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
