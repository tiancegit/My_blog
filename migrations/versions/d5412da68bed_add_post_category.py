"""add post.category

Revision ID: d5412da68bed
Revises: 848f91f61fef
Create Date: 2017-03-17 23:11:53.065674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5412da68bed'
down_revision = '848f91f61fef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('category', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'category')
    # ### end Alembic commands ###
