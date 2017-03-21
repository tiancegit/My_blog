"""del post.short_title unique

Revision ID: 2f9e03f61d4b
Revises: 9b97446637ab
Create Date: 2017-03-09 20:21:05.995100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f9e03f61d4b'
down_revision = '9b97446637ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_posts_short_title', table_name='posts')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_posts_short_title', 'posts', ['short_title'], unique=1)
    # ### end Alembic commands ###
