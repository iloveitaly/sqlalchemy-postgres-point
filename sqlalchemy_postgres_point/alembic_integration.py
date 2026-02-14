"""
Alembic integration to automatically add imports for PointType in migration files.

This module hooks into Alembic's autogenerate system to automatically include
the necessary import statement when PointType is detected in models.

Usage:
    Add this import to your alembic/env.py file:

    import sqlalchemy_postgres_point.alembic_integration

Once added, `from sqlalchemy_postgres_point import PointType` will be automatically
included in generated migration files.
"""

import alembic.autogenerate
import alembic.operations.ops
from sqlalchemy.types import UserDefinedType

from .point import PointType


def render_point_type(type_, object_, autogen_context):
    """Render PointType in migration files with proper import."""
    # Add the import to the migration file
    autogen_context.imports.add("from sqlalchemy_postgres_point import PointType")
    return "PointType()"


# Register the renderer for PointType
alembic.autogenerate.render.renderers.dispatch_for(PointType, replace=True)(
    render_point_type
)


# Also register for UserDefinedType as a fallback if the class doesn't match exactly
@alembic.autogenerate.render.renderers.dispatch_for(UserDefinedType, replace=True)
def render_user_defined_type(type_, object_, autogen_context):
    if type(object_).__name__ == "PointType":
        return render_point_type(type_, object_, autogen_context)
    return False


@alembic.autogenerate.comparators.dispatch_for("schema")
def compare_point_types(
    autogen_context: alembic.autogenerate.api.AutogenContext,
    upgrade_ops: alembic.operations.ops.UpgradeOps,
    schema_names,
):
    """
    Hook into Alembic's schema comparison to detect PointType usage.

    This ensures the import is added even if PointType is used in existing
    columns that might not trigger the render hook directly.
    """
    pass
