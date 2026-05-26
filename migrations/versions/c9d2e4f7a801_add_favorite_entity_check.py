"""add favorite entity check constraint

Revision ID: c9d2e4f7a801
Revises: 8b1d4e6f9012
Create Date: 2026-05-26 00:00:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "c9d2e4f7a801"
down_revision = "8b1d4e6f9012"
branch_labels = None
depends_on = None


CONSTRAINT_NAME = "favorite_one_entity_check"
CONSTRAINT_SQL = (
    "(CASE WHEN people_id IS NOT NULL THEN 1 ELSE 0 END) + "
    "(CASE WHEN planet_id IS NOT NULL THEN 1 ELSE 0 END) + "
    "(CASE WHEN vehicle_id IS NOT NULL THEN 1 ELSE 0 END) = 1"
)


def upgrade():
    if op.get_bind().dialect.name == "sqlite":
        with op.batch_alter_table("favorite") as batch_op:
            batch_op.create_check_constraint(CONSTRAINT_NAME, CONSTRAINT_SQL)
    else:
        op.create_check_constraint(CONSTRAINT_NAME, "favorite", CONSTRAINT_SQL)


def downgrade():
    if op.get_bind().dialect.name == "sqlite":
        with op.batch_alter_table("favorite") as batch_op:
            batch_op.drop_constraint(CONSTRAINT_NAME, type_="check")
    else:
        op.drop_constraint(CONSTRAINT_NAME, "favorite", type_="check")
