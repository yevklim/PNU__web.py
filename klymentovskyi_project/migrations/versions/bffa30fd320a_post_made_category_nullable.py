"""post: made category nullable

Revision ID: bffa30fd320a
Revises: b0b54c2b19c1
Create Date: 2023-12-12 16:44:23.684306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bffa30fd320a'
down_revision = 'b0b54c2b19c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('category_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('category_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
