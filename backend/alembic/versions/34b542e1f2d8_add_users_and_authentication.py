"""add users and authentication

Revision ID: 34b542e1f2d8
Revises: 001
Create Date: 2026-09-11 01:26:27.382342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34b542e1f2d8'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.Text(), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    op.add_column('videos', sa.Column('user_id', sa.UUID(), nullable=True))
    op.create_index(op.f('ix_videos_user_id'), 'videos', ['user_id'], unique=False)
    op.create_foreign_key('fk_videos_user_id_users', 'videos', 'users', ['user_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    op.drop_constraint('fk_videos_user_id_users', 'videos', type_='foreignkey')
    op.drop_index(op.f('ix_videos_user_id'), table_name='videos')
    op.drop_column('videos', 'user_id')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
