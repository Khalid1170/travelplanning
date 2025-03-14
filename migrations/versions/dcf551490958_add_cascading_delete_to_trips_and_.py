"""Add cascading delete to trips and activities

Revision ID: dcf551490958
Revises: 
Create Date: 2025-03-14 16:04:26.997669

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# Revision identifiers
revision = "dcf551490958"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema to add cascading delete."""

    # Modify 'activities' table
    with op.batch_alter_table("activities") as batch_op:
        # Drop existing FK constraint safely
        batch_op.drop_constraint("activities_trip_id_fkey", type_="foreignkey", if_exists=True)
        # Add new FK with CASCADE
        batch_op.create_foreign_key(
            "fk_activities_trip",
            "trips",
            ["trip_id"],
            ["id"],
            ondelete="CASCADE",
        )

    # Modify 'trips' table
    with op.batch_alter_table("trips") as batch_op:
        batch_op.drop_constraint("trips_user_id_fkey", type_="foreignkey", if_exists=True)
        batch_op.create_foreign_key(
            "fk_trips_user",
            "users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE",
        )


def downgrade() -> None:
    """Downgrade schema to remove cascading delete."""

    # Revert 'activities' table
    with op.batch_alter_table("activities") as batch_op:
        batch_op.drop_constraint("fk_activities_trip", type_="foreignkey")
        batch_op.create_foreign_key(
            "activities_trip_id_fkey",
            "trips",
            ["trip_id"],
            ["id"],
        )

    # Revert 'trips' table
    with op.batch_alter_table("trips") as batch_op:
        batch_op.drop_constraint("fk_trips_user", type_="foreignkey")
        batch_op.create_foreign_key(
            "trips_user_id_fkey",
            "users",
            ["user_id"],
            ["id"],
        )
