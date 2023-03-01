
from time import sleep
from database.database_helper import DatabaseHelper
from sensor_io.temperature_sensor import TemperatureSensor
from sensor_io.gpio_util import cleanup


if __name__ == '__main__':
    
    # An dieser Stelle kann die Pause zwischen den einzelnen Messungen eingestellt werden
    sleeptime = 1

# Hauptprogrammschleife
# Die gemessene Temperatur wird in die Konsole ausgegeben - zwischen den einzelnen Messungen
# ist eine Pause, deren Länge mit der Variable "sleeptime" eingestellt werden kann
    try:
        sensor = TemperatureSensor()
        database_helper = DatabaseHelper()

        while True:
            try:
                print('---------------------------------------')
                measurement = sensor.temperature_evaluation()
                print(f"Temperatur: {measurement.sensor_value} {measurement.sensor_unit}")
                database_helper.insert_data(measurement)
            except ValueError as v:
                print(str(v))

            sleep.sleep(sleeptime)
    except KeyboardInterrupt:
       cleanup()

