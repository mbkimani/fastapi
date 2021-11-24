"""Add users table

Revision ID: 8123cd54e60e
Revises: af356a953e5e
Create Date: 2021-11-24 13:39:11.576266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8123cd54e60e'
down_revision = 'af356a953e5e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
