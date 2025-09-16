"""

- Points should be stored as (longitude, latitude)

References:

- https://stackoverflow.com/questions/37233116/point-type-in-sqlalchemy
- https://gist.github.com/kwatch/02b1a5a8899b67df2623
- https://geoalchemy.readthedocs.io/en/0.5/intro.html
"""

import re
from typing import Optional, Tuple

from sqlalchemy.types import Float, UserDefinedType


class PointType(UserDefinedType):
    cache_ok = True

    def get_col_spec(self):
        return "POINT"

    def bind_processor(self, dialect):
        def process(bindvalue: Optional[Tuple[float, float]]):
            if bindvalue is None:
                return None
            lng, lat = bindvalue
            return f"({lng},{lat})"

        return process

    def literal_processor(self, dialect):
        def process(value: Optional[Tuple[float, float]]):
            if value is None:
                return "NULL"
            lng, lat = value
            return f"'({lng},{lat})'"

        return process

    def result_processor(self, dialect, coltype):
        def process(value: Optional[str]):
            if value is None:
                return None
            match = re.match(r"\(([^)]+),([^)]+)\)", value)
            if match:
                return (float(match.group(1)), float(match.group(2)))
            raise ValueError(f"Invalid POINT value: {value}")

        return process

    class comparator_factory(UserDefinedType.Comparator):
        def earth_distance(self, other):
            """Compute earth distance using the <@> operator, returning a Float."""
            return self.op("<@>", return_type=Float())(other)
