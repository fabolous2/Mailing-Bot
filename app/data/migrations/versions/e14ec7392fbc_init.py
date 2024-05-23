"""init

Revision ID: e14ec7392fbc
Revises: 
Create Date: 2024-05-19 17:11:11.376913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e14ec7392fbc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('gmail', sa.String(), nullable=True),
    sa.Column('password', sa.String(length=16), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('gmail'),
    sa.UniqueConstraint('password')
    )
    op.create_table('email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('audio', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('audio')
    )
    op.create_table('email_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('audio_amount', sa.Integer(), nullable=True),
    sa.Column('schedule', sa.DateTime(), nullable=True),
    sa.Column('subject', sa.String(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('turned_on', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('folder',
    sa.Column('folder_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('folder_id')
    )
    op.create_table('user_email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('sendments', sa.Integer(), nullable=False),
    sa.Column('folder_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['folder_id'], ['folder.folder_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_email')
    op.drop_table('folder')
    op.drop_table('email_settings')
    op.drop_table('email')
    op.drop_table('user')
    # ### end Alembic commands ###