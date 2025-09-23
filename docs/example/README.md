# Alembic Integration Example

This directory contains a complete example showing how the Alembic integration works.

## Files

- `models.py` - Example model using PointType
- `alembic_example.py` - Script demonstrating the integration
- `README.md` - This file

## Problem

Before the integration, when you generate Alembic migrations that use `PointType`, you would get migration files like this:

```python
def upgrade():
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', PointType(), nullable=True),  # NameError!
    sa.PrimaryKeyConstraint('id')
    )
```

This fails with `NameError: name 'PointType' is not defined` because the import is missing.

## Solution

With the integration enabled in `alembic/env.py`:

```python
import sqlalchemy_postgres_point.alembic_integration
```

The same migration becomes:

```python
from sqlalchemy_postgres_point import PointType  # Auto-added!

def upgrade():
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', PointType(), nullable=True),  # Works!
    sa.PrimaryKeyConstraint('id')
    )
```

## Usage

1. Install the package: `pip install sqlalchemy-postgres-point`
2. Add the import to your `alembic/env.py`: `import sqlalchemy_postgres_point.alembic_integration`
3. Generate migrations as usual: `alembic revision --autogenerate -m "your message"`
4. The imports will be added automatically!