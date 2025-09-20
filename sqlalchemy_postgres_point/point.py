"""

- Points should be stored as (longitude, latitude)

References:

- https://stackoverflow.com/questions/37233116/point-type-in-sqlalchemy
- https://gist.github.com/kwatch/02b1a5a8899b67df2623
- https://geoalchemy.readthedocs.io/en/0.5/intro.html
"""

import math
import re
from typing import Tuple

from sqlalchemy.types import Float, UserDefinedType


class PointType(UserDefinedType):
    cache_ok = True

    def get_col_spec(self, **kw):
        return "POINT"

    @staticmethod
    def _validate_point(value: Tuple[float, float]) -> Tuple[float, float]:
        """Validate and normalize a (lng, lat) tuple.

        - Ensures it's a 2-length tuple/list
        - Casts to float and checks finiteness (no NaN/inf)
        - Checks ranges: lng in [-180, 180], lat in [-90, 90]
        """
        try:
            lng, lat = value  # type: ignore[misc]
        except Exception as exc:  # pragma: no cover - type/len issues
            raise ValueError("Point must be a 2-tuple of (lng, lat)") from exc

        try:
            lng_f = float(lng)
            lat_f = float(lat)
        except Exception as exc:
            raise ValueError("Point coordinates must be numeric") from exc

        if not (math.isfinite(lng_f) and math.isfinite(lat_f)):
            raise ValueError("Point coordinates must be finite numbers")

        if not (-180.0 <= lng_f <= 180.0):
            raise ValueError("Longitude must be within [-180, 180]")
        if not (-90.0 <= lat_f <= 90.0):
            raise ValueError("Latitude must be within [-90, 90]")

        return (lng_f, lat_f)

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            lng, lat = self._validate_point(value)
            return f"({lng},{lat})"

        return process

    def literal_processor(self, dialect):
        def process(value):
            if value is None:
                return "NULL"
            lng, lat = self._validate_point(value)
            return f"'({lng},{lat})'"

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None:
                return None
            match = re.match(r"\(([^)]+),([^)]+)\)", value)
            if match:
                lng = float(match.group(1))
                lat = float(match.group(2))
                # Validate loaded values as well to preserve invariants in Python domain
                lng, lat = self._validate_point((lng, lat))
                return (lng, lat)
            raise ValueError(f"Invalid POINT value: {value}")

        return process

    class comparator_factory(UserDefinedType.Comparator):
        def earth_distance(self, other):
            """Compute earth distance using the <@> operator, returning a Float."""
            return self.op("<@>", return_type=Float())(other)
