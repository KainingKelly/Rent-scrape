
from sqlalchemy import Column, Float, String
from sqlalchemy.orm import declarative_base
from RentScrape.models.Base import Base


class Floorplan(Base):
    __tablename__="floorplans"

    name = Column(String, primary_key=True)
    building = Column(String, primary_key=True)
    beds = Column(String)
    baths = Column(String)
    size = Column(Float)
    img_path = Column(String)