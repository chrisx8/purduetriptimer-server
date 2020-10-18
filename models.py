from os import environ
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


# trip information table
class Trip(Base):
    __tablename__ = 'trips'
    id = Column(Integer, primary_key=True)
    from_building = Column(String(100), nullable=False)
    to_building = Column(String(100), nullable=False)
    method = Column(String(20), nullable=False)
    time = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)


# connect to DB
DATABASE_URL = environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)()
