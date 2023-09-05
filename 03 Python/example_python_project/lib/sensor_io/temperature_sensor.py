
# coding=utf-8
# Benoetigte Module werden importiert und eingerichtet
from typing import List, Optional
from .gpio_util import setup_temperature_sensor_resistance
from database.entities import SensorReading
from timesync.timesync import TimeSyncService
import glob
import time
from time import sleep


class TemperatureSensor():

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or  '/sys/bus/w1/devices/'
        setup_temperature_sensor_resistance()
        self.__wait_for_communication()
        # Zur Initialisierung, wird der Sensor einmal "blind" ausgelesen
        self.__temperature_measurement()
        self.time_sync_service = TimeSyncService()



    def __wait_for_communication(self):
        print('Warte auf Initialisierung...')
        while True:
            try:
                device_folder = glob.glob(self.base_dir + '28*')[0]
                break
            except IndexError:
                sleep(0.5)
            continue
        self.device_file = device_folder + '/w1_slave'


    # Funktion wird definiert, mit dem der aktuelle Messwert am Sensor
    # ausgelesen werden kann
    def __temperature_measurement(self) -> List[str]:
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines


    # Die Temperaturauswertung: Beim Raspberry Pi werden erkannte one-Wire Slaves im Ordner
    # /sys/bus/w1/devices/ einem eigenen Unterordner zugeordnet. In diesem Ordner befindet
    # sich die Datei w1-slave, aus der Die Daten, die über dem One-Wire Bus gesendet wurden,
    # gelesen werden können. In dieser Funktion werden diese Daten analysiert und die Temperatur
    # herausgelesen und ausgegeben
    def temperature_evaluation(self) -> SensorReading:
        lines = self.__temperature_measurement()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.__temperature_measurement()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            iso_timestamp = self.time_sync_service.get_iso_timestamp_local()
            sensor_reading = SensorReading(
                        unix_timestamp =  self.time_sync_service.get_epoc_timestamp_from_iso(iso_timestamp) * 1000,
                        iso_timestamp = iso_timestamp,
                        sensor_value = temp_c,
                        sensor_unit =  '°C'
                )
            return sensor_reading
        raise ValueError(f'the value found was no valid float {equals_pos}')
