from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import app

# connect to DB
DATABASE_URL = app.config.get('DATABASE_URL')
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)()


# trip information table
class Trip(Base):
    __tablename__ = 'trips'
    from_building = Column(String(100), nullable=False)
    to_building = Column(String(100), nullable=False)
    method = Column(String(20), nullable=False)
    time = Column(Integer, nullable=False)
