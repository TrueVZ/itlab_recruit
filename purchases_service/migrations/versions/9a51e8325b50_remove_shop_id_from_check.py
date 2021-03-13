"""Remove shop_id from check

Revision ID: 9a51e8325b50
Revises: 
Create Date: 2021-03-13 17:55:12.337838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a51e8325b50'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('check', 'shop_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('check', sa.Column('shop_id', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###