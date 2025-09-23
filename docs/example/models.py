"""Example models demonstrating PointType usage."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_postgres_point import PointType


class Base(DeclarativeBase):
    pass


class Place(Base):
    """A place with a geographic location."""
    __tablename__ = "places"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    # Location stored as (longitude, latitude)
    location = Column(PointType, nullable=True)


class Restaurant(Base):
    """A restaurant with delivery zone center."""
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    # Center of delivery zone
    delivery_center = Column(PointType, nullable=False)
    # Optional second location for chain restaurants
    second_location = Column(PointType, nullable=True)