"""empty message

Revision ID: eac610d66c04
Revises: 4d1792ce9fb6
Create Date: 2020-08-29 14:52:38.551394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eac610d66c04'
down_revision = '4d1792ce9fb6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('networks', sa.Column('tags', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('networks', 'tags')
    # ### end Alembic commands ###
