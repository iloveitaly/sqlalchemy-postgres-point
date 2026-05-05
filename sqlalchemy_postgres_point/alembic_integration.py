"""
Alembic integration for rendering PointType in generated migration files.

Usage — add two lines to your alembic/env.py:

    from sqlalchemy_postgres_point.alembic_integration import render_item

Then pass it to both context.configure() calls:

    context.configure(
        ...,
        render_item=render_item,
    )

Once wired up, ``from sqlalchemy_postgres_point import PointType`` will be
automatically included in generated migration files whenever PointType is used.
"""

from .point import PointType


def render_item(type_, obj, autogen_context):
    """Alembic render_item hook that handles PointType columns.

    Returns "PointType()" and registers the import when the rendered item is a
    PointType instance. Returns False for everything else so Alembic falls back
    to its default rendering.
    """
    if type_ == "type" and isinstance(obj, PointType):
        autogen_context.imports.add("from sqlalchemy_postgres_point import PointType")
        return "PointType()"
    return False
