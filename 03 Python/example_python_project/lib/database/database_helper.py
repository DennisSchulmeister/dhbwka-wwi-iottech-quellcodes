from database.database import Database
from pathlib import Path
from database.entities import SensorReading


class DatabaseHelper():

    def __init__(self):
        self.__database = Database(
            f'{Path(__file__).parent.parent.parent}/resources/db/sensordata.db')

    def insert_data(self, sensor_reading: SensorReading):
        self.__database.insert(sensor_reading)

    def show_data(self):
        for sensor_reading in self.__database.get_all_sensor_readings():
            print(f'{sensor_reading.id},{sensor_reading.unix_timestamp}, {sensor_reading.iso_timestamp}, {sensor_reading.sensor_value}, {sensor_reading.sensor_unit}')
