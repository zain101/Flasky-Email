"""empty message

Revision ID: 451c42358a49
Revises: 2bfd697dbd29
Create Date: 2015-04-26 21:28:55.065520

"""

# revision identifiers, used by Alembic.
revision = '451c42358a49'
down_revision = '2bfd697dbd29'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    ### end Alembic commands ###
