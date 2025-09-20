import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


def get_database_url() -> str:
    """Return database URL for tests.

    Defaults to an in-memory SQLite database when $DATABASE_URL is not set,
    so the test suite can run without external services.
    """
    return os.environ.get("DATABASE_URL", "sqlite:///:memory:")


_engine: Engine | None = None


def get_engine(echo: bool = False) -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(get_database_url(), echo=echo, future=True)
    return _engine


@contextmanager
def session_scope() -> Iterator[Session]:
    session = Session(get_engine())
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
