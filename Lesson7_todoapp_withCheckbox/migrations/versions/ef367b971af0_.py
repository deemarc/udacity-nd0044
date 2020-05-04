"""empty message

Revision ID: ef367b971af0
Revises: 129511785aaa
Create Date: 2020-05-04 01:40:06.873967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef367b971af0'
down_revision = '129511785aaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'todolist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'todolist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
