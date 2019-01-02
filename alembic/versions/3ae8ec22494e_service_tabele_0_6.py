"""service tabele 0.6

Revision ID: 3ae8ec22494e
Revises: 70f4c7eb4a04
Create Date: 2018-12-24 17:40:08.527272

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3ae8ec22494e'
down_revision = '70f4c7eb4a04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('services')
    op.drop_table('contracts')
    op.drop_table('deploy_contracts')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deploy_contracts',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('contract_name', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('address', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('tx_hash', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('deploy_time', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('pay_gas', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('contract_address', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('service_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['service_id'], ['deploy_contracts.id'], name='deploy_contracts_ibfk_1'),
    sa.PrimaryKeyConstraint('id', 'contract_name'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('contracts',
    sa.Column('contract_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('contract_address', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('contract_version', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('contract_text', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('contract_id', 'contract_address'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('services',
    sa.Column('service_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('service_name', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('service_description', mysql.VARCHAR(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('service_id', 'service_name'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###