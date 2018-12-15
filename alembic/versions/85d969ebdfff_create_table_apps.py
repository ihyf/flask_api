"""create table apps

Revision ID: 85d969ebdfff
Revises: 6c4e93bc6656
Create Date: 2018-12-13 13:20:57.690802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85d969ebdfff'
down_revision = '6c4e93bc6656'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apps',
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('apps')
    # ### end Alembic commands ###
