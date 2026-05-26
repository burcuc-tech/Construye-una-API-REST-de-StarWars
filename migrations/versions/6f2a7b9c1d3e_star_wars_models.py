"""add star wars blog models

Revision ID: 6f2a7b9c1d3e
Revises: a5cffa318ac2
Create Date: 2026-05-25 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f2a7b9c1d3e'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('first_name', sa.String(length=80), nullable=False, server_default=''))
    op.add_column('user', sa.Column('last_name', sa.String(length=80), nullable=False, server_default=''))

    op.create_table(
        'people',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('gender', sa.String(length=40), nullable=False),
        sa.Column('height', sa.String(length=40), nullable=False),
        sa.Column('eye_color', sa.String(length=40), nullable=False),
        sa.Column('hair_color', sa.String(length=40), nullable=False),
        sa.Column('birth_year', sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'planet',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('population', sa.String(length=80), nullable=False),
        sa.Column('climate', sa.String(length=120), nullable=False),
        sa.Column('terrain', sa.String(length=120), nullable=False),
        sa.Column('diameter', sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'favorite',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('people_id', sa.Integer(), nullable=True),
        sa.Column('planet_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['people_id'], ['people.id']),
        sa.ForeignKeyConstraint(['planet_id'], ['planet.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('favorite')
    op.drop_table('planet')
    op.drop_table('people')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
