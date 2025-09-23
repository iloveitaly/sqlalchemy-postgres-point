# Alembic Integration

When using `PointType` in your SQLAlchemy models, you need to ensure that Alembic migration files include the proper import statement. This package provides automatic integration with Alembic to handle this for you.

## Setup

To enable automatic import generation for `PointType` in your Alembic migrations, simply add this import to your `alembic/env.py` file:

```python
# alembic/env.py
import sqlalchemy_postgres_point.alembic_integration
```

That's it! Now when you generate migrations containing `PointType`, the import will be automatically added.

## Example

### 1. Model Definition

**models.py**
```python
from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_postgres_point import PointType

class Base(DeclarativeBase):
    pass

class Place(Base):
    __tablename__ = "places"
    
    id = Column(Integer, primary_key=True)
    location = Column(PointType)
```

### 2. Alembic Configuration

**alembic/env.py**
```python
from alembic import context
from sqlalchemy import engine_from_config, pool

# Import the integration (this enables auto-import functionality)
import sqlalchemy_postgres_point.alembic_integration

# Import your models
from myproject.models import Base

# ... rest of your env.py configuration
target_metadata = Base.metadata
```

### 3. Generate Migration

```bash
alembic revision --autogenerate -m "Add place table with location"
```

### 4. Generated Migration (with auto-import)

The generated migration file will automatically include the necessary import:

```python
"""Add place table with location

Revision ID: abc123
Revises: 
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_postgres_point import PointType

# revision identifiers, used by Alembic.
revision = 'abc123'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', PointType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('places')
```

## Without Integration

Without this integration, you would get migration files like this (which would fail):

```python
# This would fail because PointType is not imported
def upgrade():
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', PointType(), nullable=True),  # NameError: name 'PointType' is not defined
    sa.PrimaryKeyConstraint('id')
    )
```

## How It Works

The integration uses Alembic's plugin system to:

1. **Register a Type Renderer**: When Alembic encounters a `PointType` in your models, our custom renderer is called
2. **Add Import Statement**: The renderer automatically adds `from sqlalchemy_postgres_point import PointType` to the migration file's imports
3. **Render Type**: The renderer returns the proper type representation: `PointType()`

This approach is similar to how other SQLAlchemy extensions like `alembic-postgresql-enum` work, providing seamless integration with Alembic's autogenerate functionality.