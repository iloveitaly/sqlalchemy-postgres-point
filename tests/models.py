from typing import Optional, Tuple

from sqlalchemy import Column
from sqlmodel import Field, SQLModel

from sqlalchemy_postgres_point import PointType


class Place(SQLModel, table=True):  # type: ignore[call-arg]
    __tablename__ = "places"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    # Stored as PostgreSQL POINT, interpreted as (lng, lat)
    # Use sa_column to inject a SQLAlchemy Column with our custom type
    location: Optional[Tuple[float, float]] = Field(
        default=None,
        sa_column=Column(PointType()),
    )
    name: str = Field(default="")
