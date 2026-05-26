"""add vehicle model

Revision ID: 8b1d4e6f9012
Revises: 6f2a7b9c1d3e
Create Date: 2026-05-25 00:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b1d4e6f9012'
down_revision = '6f2a7b9c1d3e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'vehicle',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('model', sa.String(length=120), nullable=False),
        sa.Column('manufacturer', sa.String(length=180), nullable=False),
        sa.Column('vehicle_class', sa.String(length=80), nullable=False),
        sa.Column('crew', sa.String(length=40), nullable=False),
        sa.Column('passengers', sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column('favorite', sa.Column('vehicle_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'favorite', 'vehicle', ['vehicle_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'favorite', type_='foreignkey')
    op.drop_column('favorite', 'vehicle_id')
    op.drop_table('vehicle')
