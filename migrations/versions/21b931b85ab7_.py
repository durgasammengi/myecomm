"""empty message

Revision ID: 21b931b85ab7
Revises: d74f74417d88
Create Date: 2023-09-20 12:49:19.558836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21b931b85ab7'
down_revision = 'd74f74417d88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('name', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'name')
    # ### end Alembic commands ###
