from sqlalchemy import Column, Date, Float, ForeignKey, String
from sqlalchemy.orm import declarative_base
from RentScrape.models.Base import Base


class Unit(Base):
    __tablename__ = "units"

    unit_number = Column(String, primary_key = True)
    as_of = Column(Date, primary_key = True)
    building = Column(String, primary_key = True)
    floorplan = Column(String, ForeignKey("floorplans.name"))
    price = Column(Float)
    data_available = Column(Date)
