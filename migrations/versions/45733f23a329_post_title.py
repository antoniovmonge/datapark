"""post title

Revision ID: 45733f23a329
Revises: a8df0ccc2bdc
Create Date: 2021-10-23 15:27:03.083776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45733f23a329'
down_revision = 'a8df0ccc2bdc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('title', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'title')
    # ### end Alembic commands ###