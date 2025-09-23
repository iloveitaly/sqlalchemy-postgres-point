# Alembic Integration

When using `PointType` in your SQLAlchemy models, add this import to your `alembic/env.py` file:

**alembic/env.py**
```python
import sqlalchemy_postgres_point.alembic_integration
```

This automatically adds `from sqlalchemy_postgres_point import PointType` to migration files when `PointType` is detected in your models.