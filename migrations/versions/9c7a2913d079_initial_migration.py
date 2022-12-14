"""Initial Migration

Revision ID: 9c7a2913d079
Revises: 
Create Date: 2022-09-06 20:45:11.648427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c7a2913d079'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('business')
    op.drop_column('post', 'business')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('business', sa.VARCHAR(length=150), autoincrement=False, nullable=False))
    op.create_table('business',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('zipcode', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='business_pkey')
    )
    # ### end Alembic commands ###
