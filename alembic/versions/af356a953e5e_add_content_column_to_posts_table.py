"""add content column to posts table

Revision ID: af356a953e5e
Revises: cd01c517eb77
Create Date: 2021-11-23 15:42:04.495753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af356a953e5e'
down_revision = 'cd01c517eb77'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
