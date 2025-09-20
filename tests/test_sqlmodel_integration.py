import pytest
from sqlalchemy import select
from sqlmodel import SQLModel

from tests.db import get_engine
from tests.models import Place


@pytest.fixture(scope="module")
def engine():
    eng = get_engine()
    SQLModel.metadata.drop_all(eng)
    SQLModel.metadata.create_all(eng)
    return eng


def test_insert_and_select_point(engine):
    from sqlalchemy.orm import Session

    with Session(engine) as session:
        p = Place(name="Test", location=(1.0, 2.0))
        session.add(p)
        session.commit()
        session.refresh(p)
        assert p.id is not None

    with Session(engine) as session:
        row = session.get(Place, p.id)
        assert row is not None
        assert row.location == (1.0, 2.0)


def test_distance_operator_compiles(engine):
    # Only check SQL compilation because the <@> operator may require extensions
    # Access the column attribute from the SQLModel table to get the comparator
    stmt = select(Place.__table__.c.location.earth_distance((3.0, 4.0)))  # type: ignore[attr-defined]
    compiled = stmt.compile(engine)
    sql_text = str(compiled)
    assert "<@>" in sql_text
    assert "places" in sql_text
