"""update table apps v3

Revision ID: 99575a844f61
Revises: 01f2295cdf93
Create Date: 2018-12-13 11:22:11.352199

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '99575a844f61'
down_revision = '01f2295cdf93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('apps', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apps', sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False))
    # ### end Alembic commands ###
