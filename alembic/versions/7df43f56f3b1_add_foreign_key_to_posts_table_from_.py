"""add foreign key to posts table from users

Revision ID: 7df43f56f3b1
Revises: 8123cd54e60e
Create Date: 2021-11-24 14:11:03.780385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7df43f56f3b1'
down_revision = '8123cd54e60e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
