"""Test sqlalchemy-postgres-point."""

import sqlalchemy_postgres_point


def test_import() -> None:
    """Test that the  can be imported."""
    assert isinstance(sqlalchemy_postgres_point.__name__, str)
