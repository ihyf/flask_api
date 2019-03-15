"""201903101420

Revision ID: 3c15f94b20d0
Revises: a3aaefef5d7f
Create Date: 2019-03-14 14:20:03.804293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c15f94b20d0'
down_revision = 'a3aaefef5d7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction_record', sa.Column('tr_appid', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction_record', 'tr_appid')
    # ### end Alembic commands ###
