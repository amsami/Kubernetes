"""empty message

Revision ID: 71aaeacad3d8
Revises: 
Create Date: 2020-03-16 12:08:07.386339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71aaeacad3d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todos')
    # ### end Alembic commands ###
