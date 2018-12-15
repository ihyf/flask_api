"""update table apps2

Revision ID: c37b22345bcf
Revises: bff12bd9168c
Create Date: 2018-12-13 13:16:52.916802

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c37b22345bcf'
down_revision = 'bff12bd9168c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apps2',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('appid', sa.String(length=200), nullable=False),
    sa.Column('desc', sa.String(length=200), nullable=False),
    sa.Column('ip', sa.JSON(), nullable=False),
    sa.Column('ns', sa.JSON(), nullable=False),
    sa.Column('cli_publickey', sa.Text(), nullable=False),
    sa.Column('cli_privatekey', sa.Text(), nullable=False),
    sa.Column('srv_publickey', sa.Text(), nullable=False),
    sa.Column('srv_privatekey', sa.Text(), nullable=False),
    sa.Column('srv', sa.JSON(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'appid'),
    sa.UniqueConstraint('appid')
    )
    op.drop_table('123')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('123',
    sa.Column('n1', mysql.INTEGER(display_width=10, unsigned=True), autoincrement=True, nullable=False),
    sa.Column('n2', mysql.CHAR(length=50), nullable=False),
    sa.Column('n3', mysql.CHAR(length=50), nullable=True),
    sa.Column('n4', mysql.CHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('n1', 'n2'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('apps2')
    # ### end Alembic commands ###
