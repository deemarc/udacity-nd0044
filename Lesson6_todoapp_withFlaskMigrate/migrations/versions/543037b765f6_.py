"""empty message

Revision ID: 543037b765f6
Revises: afab470e585e
Create Date: 2020-05-02 15:29:04.587705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '543037b765f6'
down_revision = 'afab470e585e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))

    op.execute('UPDATE todos SET completed = False WHERE completed is NULL;')

    op.alter_column('todos', 'completed', nullable=False)

    # ### end Alembic commands ###
    


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
