"""add film model

Revision ID: 5140619be307
Revises: 
Create Date: 2024-03-08 15:50:01.838371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5140619be307'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('films',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('release_date', sa.Date(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('distributed_by', sa.String(length=128), nullable=False),
    sa.Column('length', sa.Float(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('films')
    # ### end Alembic commands ###
