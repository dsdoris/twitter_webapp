"""empty message

Revision ID: de4b4aa4998d
Revises: 
Create Date: 2020-12-02 11:11:02.350381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de4b4aa4998d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('followers', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('tweet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('embedding', sa.PickleType(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('passenger')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('passenger',
    sa.Column('survived', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('pclass', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('sex', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('age', sa.REAL(), autoincrement=False, nullable=True),
    sa.Column('siblings_spouses_aboard', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('parents_children_aboard', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('fare', sa.REAL(), autoincrement=False, nullable=True)
    )
    op.drop_table('tweet')
    op.drop_table('user')
    # ### end Alembic commands ###