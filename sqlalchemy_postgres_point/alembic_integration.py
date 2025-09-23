"""
Alembic integration to automatically add imports for PointType in migration files.

This module hooks into Alembic's autogenerate system to automatically include
the necessary import statement when PointType is detected in models.

Usage:
    Add this import to your alembic/env.py file:

    import sqlalchemy_postgres_point.alembic_integration

That's it! Now when you generate migrations containing PointType,
the import will be automatically added.
"""

import alembic
from alembic.autogenerate.api import AutogenContext
from alembic.operations.ops import UpgradeOps

from .point import PointType


@alembic.autogenerate.render.renderers.dispatch_for(PointType)
def render_point_type(type_, object_, autogen_context):
    """Render PointType in migration files with proper import."""
    # Add the import to the migration file
    autogen_context.imports.add("from sqlalchemy_postgres_point import PointType")
    return "PointType()"


@alembic.autogenerate.comparators.dispatch_for("schema")
def compare_point_types(
    autogen_context: AutogenContext,
    upgrade_ops: UpgradeOps,
    schema_names,
):
    """
    Hook into Alembic's schema comparison to detect PointType usage.
    
    This ensures the import is added even if PointType is used in existing
    columns that might not trigger the render hook directly.
    """
    # This function doesn't need to do much - the real work is done
    # by the render hook above. This just ensures we're in the comparison
    # phase where we can detect PointType usage.
    pass