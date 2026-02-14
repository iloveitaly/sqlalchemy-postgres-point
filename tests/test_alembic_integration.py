import os
import shutil
from pathlib import Path
from typing import Optional, Tuple

from alembic import command
from alembic.config import Config
from sqlalchemy import Column
from sqlmodel import Field, SQLModel

from sqlalchemy_postgres_point import PointType


class AlembicTestModel(SQLModel, table=True):
    __tablename__ = "alembic_test_model"
    id: Optional[int] = Field(default=None, primary_key=True)
    location: Optional[Tuple[float, float]] = Field(
        default=None,
        sa_column=Column(PointType()),
    )


def test_alembic_integration():
    test_root = Path(__file__).parent
    alembic_root = test_root / "alembic_test_env"
    versions_path = alembic_root / "versions"

    # Ensure versions directory exists and is empty
    if versions_path.exists():
        shutil.rmtree(versions_path)
    versions_path.mkdir(parents=True)

    # Configure Alembic
    alembic_cfg = Config(str(alembic_root / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(alembic_root))
    alembic_cfg.set_main_option("sqlalchemy.url", "sqlite:///:memory:")

    # Generate a revision with autogenerate enabled
    command.revision(alembic_cfg, message="test migration", autogenerate=True)

    # Find the generated migration file
    migration_files = [f for f in os.listdir(str(versions_path)) if f.endswith(".py")]
    assert len(migration_files) == 1
    migration_path = versions_path / migration_files[0]

    with open(migration_path, "r") as f:
        content = f.read()

    # Verify the import is present
    assert "from sqlalchemy_postgres_point import PointType" in content
    # Verify the type is rendered correctly
    assert "PointType()" in content

    # Cleanup
    shutil.rmtree(versions_path)
    versions_path.mkdir()


def test_render_point_type_directly():
    from sqlalchemy_postgres_point.alembic_integration import render_point_type

    class MockAutogenContext:
        def __init__(self):
            self.imports = set()

    ctx = MockAutogenContext()
    result = render_point_type(PointType(), None, ctx)

    assert result == "PointType()"
    assert "from sqlalchemy_postgres_point import PointType" in ctx.imports
