"""contribution model modified again

Revision ID: a7df3c829b0c
Revises: a864afa6d964
Create Date: 2025-01-17 12:45:08.327777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a7df3c829b0c'
down_revision: Union[str, None] = 'a864afa6d964'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ProjectContribution')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ProjectContribution',
    sa.Column('project_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('total', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['Project.id'], name='ProjectContribution_project_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='ProjectContribution_pkey')
    )
    # ### end Alembic commands ###