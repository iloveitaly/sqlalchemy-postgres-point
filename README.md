sqlalchemy-postgres-point
=========================

Lightweight, pure-Python SQLAlchemy custom type for PostgreSQL `POINT` columns.

Why
----

PostgreSQL has a native `POINT` type (stored internally as a pair of float8 values). SQLAlchemy does not ship a dedicated high-level type wrapper for simple geometric primitives. This package provides a very small `PointType` you can use immediately without pulling in a full spatial stack (e.g. PostGIS + GeoAlchemy2) when all you need is storing and retrieving `(longitude, latitude)` pairs.

Features
--------

* Simple `(lng, lat)` tuple binding and result conversion.
* Safe NULL handling.
* Literal rendering for DDL / SQL emission.
* Custom comparator exposing the PostgreSQL earth-distance `<@>` operator (returns a `Float`).
* `cache_ok = True` for SQLAlchemy 2.x compilation caching.

Installation
------------

Using `uv` (recommended):

```bash
uv add sqlalchemy-postgres-point
```

Or with pip:

```bash
pip install sqlalchemy-postgres-point
```

Usage
-----

```python
from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_postgres_point import PointType


class Base(DeclarativeBase):
	pass


class Place(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True)
    # Store as (longitude, latitude)
    location = Column(PointType)

# Example query using the custom comparator
from sqlalchemy import select

origin = (0.0, 0.0)
stmt = select(Place.id, Place.location.earth_distance(origin).label("dist"))
```

The comparator translates `Place.location.earth_distance(origin)` into SQL using the `<@>` operator (requires PostgreSQL with the `cube` / `earthdistance` extension for meaningful results; without extensions the operator may not exist—adapt as needed for your environment). This library only *emits* the operator; it does not manage PostgreSQL extensions.

## PostgreSQL Extensions Setup

To use the earth distance functionality (`earth_distance()` comparator), you need to enable the `cube` and `earthdistance` PostgreSQL extensions. These extensions provide spatial operations for calculating distances between geographic points on Earth's surface using a spherical model.

### Alembic Migration Example

If you're using Alembic for database migrations, you can create a migration to enable these extensions:

```python
"""Add PostgreSQL extensions for earth distance calculations

Revision ID: your_revision_id
Revises: your_previous_revision
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'your_revision_id'
down_revision: Union[str, None] = 'your_previous_revision'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
CREATE EXTENSION IF NOT EXISTS cube;
CREATE EXTENSION IF NOT EXISTS earthdistance;
""")


def downgrade() -> None:
    op.execute("""
DROP EXTENSION IF EXISTS earthdistance;
DROP EXTENSION IF EXISTS cube;
""")
```

**Integration Steps:**

1. Generate a new migration: `alembic revision -m "add_postgres_extensions"`
2. Copy the `upgrade()` and `downgrade()` functions above into your new migration file
3. Run the migration: `alembic upgrade head`

Returned Python Values
----------------------

Values are loaded as a 2-tuple of floats `(lng, lat)` or `None` when NULL.

Testing
-------

Run the test suite with:

```bash
uv run pytest -q
```

Development
-----------

After cloning:

```bash
uv sync  # installs runtime + dev deps
uv run pytest -q
```

Project Structure
-----------------

* `sqlalchemy_postgres_point/point.py` – Implementation of `PointType`.
* `tests/test_point.py` – Unit tests for processors and comparator.

Limitations / Notes
-------------------

* No automatic validation of longitude/latitude ranges; add your own if required.
* Uses simple textual representation `(lng,lat)` accepted by PostgreSQL `POINT` input parser.
* If you need advanced spatial indexing / SRID support, look at GeoAlchemy2/PostGIS instead.

License
-------

MIT (see your project's LICENSE file if added later). Contributions welcome.

