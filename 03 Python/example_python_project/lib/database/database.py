import logging
from typing import List
from sqlalchemy import create_engine
from sqlite3 import IntegrityError
from sqlalchemy.orm import sessionmaker
from .entities import Base, SensorReading

class Database():

    def __init__(self, database_path: str):
        engine = create_engine(url=f'sqlite:///{database_path}', connect_args={'timeout': 10})
        Base.metadata.create_all(engine)
        self.__session_maker = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        self.__logger = logging.getLogger('db_core')

    def __create_session(self):
        return self.__session_maker()

    def get_all_sensor_readings(self) -> List[SensorReading]:
        with self.__create_session() as session:
            return session.execute(session.query(SensorReading)).scalars().all()

    def insert(self, sensor_reading: SensorReading):
        with self.__create_session() as session:
            try:
                with session.begin():
                    session.add(sensor_reading)
                    session.commit()
              
            except IntegrityError as integrity_error:
                self.__logger.info(f"Warning: Database: {str(integrity_error)}")

            except TypeError as type_error:
                self.__logger.warning(str(type_error))

            except Exception as error:
                self.__logger.error(f"Database thread error: {str(error)}")
