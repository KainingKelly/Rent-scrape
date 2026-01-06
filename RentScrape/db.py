from sqlalchemy import create_engine
from models.Base import Base

import models.floorplan
import models.unit
# https://username:password@url:port/path
engine = create_engine("postgresql://kaining:mypassword@localhost:5432/rentscrapedb")

Base.metadata.create_all(engine)