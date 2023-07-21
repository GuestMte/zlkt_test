"""empty message

Revision ID: a9ac74a25fd5
Revises: 858ec4232b43
Create Date: 2023-07-20 01:05:57.639696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9ac74a25fd5'
down_revision = '858ec4232b43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('captcha', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email')
    # ### end Alembic commands ###
