"""add relationship many-to-many

Revision ID: 719cf3d46910
Revises: f0a447082ebc
Create Date: 2024-03-10 15:11:26.950471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '719cf3d46910'
down_revision = 'f0a447082ebc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movies_actors',
    sa.Column('actor_id', sa.Integer(), nullable=False),
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
    sa.ForeignKeyConstraint(['film_id'], ['films.id'], ),
    sa.PrimaryKeyConstraint('actor_id', 'film_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies_actors')
    # ### end Alembic commands ###