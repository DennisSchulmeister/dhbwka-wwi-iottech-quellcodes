from database.entities import SensorReading
import time
from datetime import datetime

class SensorDummy():

    def read_value(self) -> SensorReading:
        print('Eingabe des simulierten Sensorwertes:')
        timestamp = round(time.time() * 1000)
        return SensorReading(
            unix_timestamp=timestamp,
            iso_timestamp=datetime.fromtimestamp(
                timestamp / 1000).astimezone().isoformat(),
            sensor_value=input(),
            sensor_unit='°C'
        )