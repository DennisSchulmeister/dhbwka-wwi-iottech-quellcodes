from dataclasses import dataclass
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

@dataclass
class SensorReading(Base):
    __tablename__ = 'sensor_reading'
    id = Column(Integer, primary_key=True, autoincrement=True)
    unix_timestamp = Column(Integer)
    iso_timestamp = Column(String)
    sensor_value = Column(Integer)
    sensor_unit =  Column(String)