
from sensor_io.sensor_dummy import SensorDummy
from database.entities import SensorReading
from pytest import MonkeyPatch
from time import time
from datetime import datetime

def test_read_value(monkeypatch: MonkeyPatch):
     sensor = SensorDummy()
     monkeypatch.setattr('builtins.input', lambda: 42)
     value: SensorReading = sensor.read_value()
     assert value.unix_timestamp > round(time() * 1000) - 2000
     assert datetime.fromisoformat(str(value.iso_timestamp)).timestamp() * 1000 == value.unix_timestamp
     assert value.sensor_unit == '°C'
     assert value.sensor_value == 42