"""xxx

Revision ID: 619fdd628ccb
Revises: bd09f017ad7e
Create Date: 2019-03-13 10:05:10.549384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '619fdd628ccb'
down_revision = 'bd09f017ad7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recode_logs',
    sa.Column('rl_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.Column('level_name', sa.String(length=10), nullable=True),
    sa.Column('message', sa.String(length=255), nullable=True),
    sa.Column('splilt_type', sa.String(length=10), nullable=True),
    sa.Column('split_base', sa.String(length=10), nullable=True),
    sa.Column('exc_info', sa.String(length=255), nullable=True),
    sa.Column('exc_text', sa.String(length=255), nullable=True),
    sa.Column('file_name', sa.String(length=100), nullable=True),
    sa.Column('line_no', sa.Integer(), nullable=True),
    sa.Column('func_name', sa.String(length=255), nullable=True),
    sa.Column('stack_info', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('rl_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recode_logs')
    # ### end Alembic commands ###