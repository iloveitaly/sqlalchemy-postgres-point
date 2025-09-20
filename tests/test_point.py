import re

import pytest
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import column, select

from sqlalchemy_postgres_point import PointType


def test_bind_processor():
    pt = PointType()
    proc = pt.bind_processor(None)
    assert proc((1.23, 4.56)) == "(1.23,4.56)"
    assert proc(None) is None


def test_literal_processor():
    pt = PointType()
    proc = pt.literal_processor(None)
    assert proc((1.23, 4.56)) == "'(1.23,4.56)'"
    assert proc(None) == "NULL"


def test_result_processor_valid():
    pt = PointType()
    proc = pt.result_processor(None, None)
    assert proc("(1.23,4.56)") == (1.23, 4.56)
    assert proc(None) is None


def test_result_processor_invalid():
    pt = PointType()
    proc = pt.result_processor(None, None)
    with pytest.raises(ValueError):
        proc("invalid")


def test_validation_bind_out_of_range():
    pt = PointType()
    bind = pt.bind_processor(None)
    with pytest.raises(ValueError):
        bind((200.0, 0.0))  # invalid longitude
    with pytest.raises(ValueError):
        bind((0.0, 100.0))  # invalid latitude


def test_validation_literal_non_finite():
    import math

    pt = PointType()
    lit = pt.literal_processor(None)
    with pytest.raises(ValueError):
        lit((math.nan, 0.0))
    with pytest.raises(ValueError):
        lit((0.0, math.inf))


def test_validation_result_out_of_range():
    pt = PointType()
    res = pt.result_processor(None, None)
    with pytest.raises(ValueError):
        res("(181,0)")
    with pytest.raises(ValueError):
        res("(0,91)")


def test_earth_distance_compilation():
    # Build an expression using the custom comparator
    c = column("location", PointType())
    other_point = (10.0, 20.0)
    expr = c.earth_distance(other_point)
    stmt = select(expr)
    compiled = stmt.compile(dialect=postgresql.dialect())
    sql = str(compiled)
    # Expect the <@> operator to appear between the column and a bind / literal
    assert "<@>" in sql
    # Ensure the POINT literal/bind shape is present
    assert re.search(r"location\s*<@>", sql)
