[![Release Notes](https://img.shields.io/github/release/iloveitaly/sqlalchemy-postgres-point)](https://github.com/iloveitaly/sqlalchemy-postgres-point/releases)
[![Downloads](https://static.pepy.tech/badge/sqlalchemy-postgres-point/month)](https://pepy.tech/project/sqlalchemy-postgres-point)
![GitHub CI Status](https://github.com/iloveitaly/sqlalchemy-postgres-point/actions/workflows/build_and_publish.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# sqlalchemy-postgres-point

Lightweight, pure-Python SQLAlchemy custom type for PostgreSQL `POINT` columns.

## Why

PostgreSQL has a native `POINT` type (stored internally as a pair of float8 values). SQLAlchemy does not ship a dedicated high-level type wrapper for simple geometric primitives. This package provides a very small `PointType` you can use immediately without pulling in a full spatial stack (e.g. PostGIS + GeoAlchemy2) when all you need is storing and retrieving `(longitude, latitude)` pairs.

## Features

* Simple `(lng, lat)` tuple binding and result conversion.
* Safe NULL handling.
* Literal rendering for DDL / SQL emission.
* Custom comparator exposing the PostgreSQL earth-distance `<@>` operator (returns a `Float`).
* `cache_ok = True` for SQLAlchemy 2.x compilation caching.

## Installation

```bash
uv add sqlalchemy-postgres-point
```

## Usage

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

#### Integration Steps

1. Generate a new migration: `alembic revision -m "add_postgres_extensions"`
2. Copy the `upgrade()` and `downgrade()` functions above into your new migration file
3. Run the migration: `alembic upgrade head`

## Returned Python Values

Values are loaded as a 2-tuple of floats `(lng, lat)` or `None` when NULL.

## Alembic Integration

To ensure generated migration files include the correct `PointType` import, pass the provided `render_item` hook to `context.configure()` in your `alembic/env.py`:

```python
from sqlalchemy_postgres_point.alembic_integration import render_item

# in run_migrations_online and run_migrations_offline:
context.configure(
    # ... other options ...
    render_item=render_item,
)
```

Once wired up, `from sqlalchemy_postgres_point import PointType` will be automatically included in generated migration files whenever a `PointType` column is detected.

### Chaining `render_item`

It's insane to me, but you have to chain multiple `render_item` instances you may have yourself.

```python
from sqlalchemy_postgres_point.alembic_integration import render_item as render_point

def render_item(type_, obj, autogen_context):
    return (
        render_point(type_, obj, autogen_context)
        or other_package.render_item(type_, obj, autogen_context)
        or False
    )
```

Or you could use something like [`some_fn`](https://funcy.readthedocs.io/en/stable/funcs.html#some_fn) to make this even cleaner.

## Limitations / Notes

* No automatic validation of longitude/latitude ranges; add your own if required.
* Uses simple textual representation `(lng,lat)` accepted by PostgreSQL `POINT` input parser.
* If you need advanced spatial indexing / SRID support, look at GeoAlchemy2/PostGIS instead.

---

*This project was created from [iloveitaly/python-package-template](https://github.com/iloveitaly/python-package-template)*
