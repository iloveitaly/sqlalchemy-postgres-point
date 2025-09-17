from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

DEFAULT_TEST_DB = "postgresql+psycopg://root:password@localhost:5432/development"


def get_database_url() -> str:
    return os.environ.get("TEST_DATABASE_URL", DEFAULT_TEST_DB)


_engine: Engine | None = None


def get_engine(echo: bool = False) -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(get_database_url(), echo=echo, future=True)
    return _engine


def database_available() -> bool:
    try:
        eng = get_engine()
        with eng.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError:
        return False
    except Exception:
        if os.environ.get("DEBUG_DB"):
            raise
        return False


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
