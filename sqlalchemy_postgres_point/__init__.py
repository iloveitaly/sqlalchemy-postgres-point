"""Top-level package for `sqlalchemy-postgres-point`.

Exports:
    PointType: SQLAlchemy custom type representing a PostgreSQL POINT column.
"""

from .point import PointType

__all__ = [
    "PointType",
]
