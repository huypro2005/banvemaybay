"""dat ten bang nhan vien

Revision ID: 44fabf92fb5a
Revises: 8af311092157
Create Date: 2025-03-20 12:11:41.791633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44fabf92fb5a'
down_revision = '8af311092157'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('nhanvien')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nhanvien',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=80), nullable=True),
    sa.Column('username', sa.VARCHAR(length=50), nullable=True),
    sa.Column('password', sa.TEXT(), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('pos', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###
