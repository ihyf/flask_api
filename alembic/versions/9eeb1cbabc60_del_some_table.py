"""del some table

Revision ID: 9eeb1cbabc60
Revises: c37b22345bcf
Create Date: 2018-12-13 13:18:35.636677

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9eeb1cbabc60'
down_revision = 'c37b22345bcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('appid', table_name='apps2')
    op.drop_table('apps2')
    op.drop_table('zzy_key2')
    op.drop_table('zzy_key3')
    op.drop_table('zzy_key')
    op.add_column('apps', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('apps', 'id')
    op.create_table('zzy_key',
    sa.Column('name', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('update', mysql.DATETIME(), nullable=True),
    sa.Column('private_key', mysql.TEXT(), nullable=True),
    sa.Column('public_key', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('name'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('zzy_key3',
    sa.Column('name', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('update', mysql.DATETIME(), nullable=True),
    sa.Column('private_key', mysql.TEXT(), nullable=True),
    sa.Column('public_key', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('name'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('zzy_key2',
    sa.Column('name', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('update', mysql.DATETIME(), nullable=True),
    sa.Column('private_key', mysql.TEXT(), nullable=True),
    sa.Column('public_key', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('name'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('apps2',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('appid', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('desc', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('ip', mysql.JSON(), nullable=False),
    sa.Column('ns', mysql.JSON(), nullable=False),
    sa.Column('cli_publickey', mysql.TEXT(), nullable=False),
    sa.Column('cli_privatekey', mysql.TEXT(), nullable=False),
    sa.Column('srv_publickey', mysql.TEXT(), nullable=False),
    sa.Column('srv_privatekey', mysql.TEXT(), nullable=False),
    sa.Column('srv', mysql.JSON(), nullable=False),
    sa.Column('status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', 'appid'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('appid', 'apps2', ['appid'], unique=True)
    # ### end Alembic commands ###
