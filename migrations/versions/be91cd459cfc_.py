"""empty message

Revision ID: be91cd459cfc
Revises: 6a0c28a7308c
Create Date: 2022-06-02 15:23:52.791269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be91cd459cfc'
down_revision = '6a0c28a7308c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###