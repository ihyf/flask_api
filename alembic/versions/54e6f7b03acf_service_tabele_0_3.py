"""service tabele 0.3

Revision ID: 54e6f7b03acf
Revises: 866e95aa7b65
Create Date: 2018-12-24 15:31:02.909248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54e6f7b03acf'
down_revision = '866e95aa7b65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contracts', sa.Column('contract_version', sa.String(length=20), nullable=True))
    op.add_column('services', sa.Column('service_description', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('services', 'service_description')
    op.drop_column('contracts', 'contract_version')
    # ### end Alembic commands ###
