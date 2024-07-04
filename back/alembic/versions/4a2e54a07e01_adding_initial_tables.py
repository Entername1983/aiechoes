"""adding initial tables

Revision ID: 4a2e54a07e01
Revises: d8004db4651f
Create Date: 2024-07-02 09:01:30.906534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a2e54a07e01'
down_revision: Union[str, None] = 'd8004db4651f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('image_url', sa.String(length=255), nullable=False),
    sa.Column('thumbnail_url', sa.String(length=255), nullable=True),
    sa.Column('time_created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('replies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time_created', sa.DateTime(), nullable=False),
    sa.Column('model', sa.String(length=50), nullable=False),
    sa.Column('reply', sa.String(length=512), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('replies')
    op.drop_table('images')
    # ### end Alembic commands ###
