"""create posts table

Revision ID: cd01c517eb77
Revises: 
Create Date: 2021-11-23 15:20:35.416182

"""
from re import T
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Integer


# revision identifiers, used by Alembic.
revision = 'cd01c517eb77'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
