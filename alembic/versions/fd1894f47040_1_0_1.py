"""1.0.1

Revision ID: fd1894f47040
Revises: 2100966bfa5e
Create Date: 2018-12-10 11:51:26.332426

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fd1894f47040'
down_revision = '2100966bfa5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('zzy_key',
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('update', sa.DATETIME(), nullable=True),
    sa.Column('private_key', sa.Text(), nullable=True),
    sa.Column('public_key', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('zzy_key2',
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('update', sa.DATETIME(), nullable=True),
    sa.Column('private_key', sa.Text(), nullable=True),
    sa.Column('public_key', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.drop_table('apps2')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apps2',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('app_name', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('app_desc', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('app_ip', mysql.JSON(), nullable=True),
    sa.Column('app_ns', mysql.JSON(), nullable=True),
    sa.Column('app_publickey', mysql.TEXT(), nullable=True),
    sa.Column('app_privateKey', mysql.TEXT(), nullable=True),
    sa.Column('app_function', mysql.JSON(), nullable=True),
    sa.Column('app_status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('app_request_times', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', 'app_name'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('zzy_key2')
    op.drop_table('zzy_key')
    # ### end Alembic commands ###