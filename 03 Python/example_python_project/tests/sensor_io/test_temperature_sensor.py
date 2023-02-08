import os
from time import time
from datetime import datetime


def test_temperature_evaluation(monkeypatch):
    monkeypatch.setattr('sensor_io.gpio_util.setup_temperature_sensor_resistance', lambda: print('patched'))
    from sensor_io.temperature_sensor import TemperatureSensor

    test_data_dir = f'{os.path.dirname(__file__)}/data/'
    temperature_sensor = TemperatureSensor(test_data_dir)

    measurement = temperature_sensor.temperature_evaluation()
    assert measurement.unix_timestamp > round(time() * 1000) - 2000
    assert datetime.fromisoformat(str(measurement.iso_timestamp)).timestamp() * 1000 == measurement.unix_timestamp
    assert measurement.sensor_unit == '°C'
    assert measurement.sensor_value == 25.625
