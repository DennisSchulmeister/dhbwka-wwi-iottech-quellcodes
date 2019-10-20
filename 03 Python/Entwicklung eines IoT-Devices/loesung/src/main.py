#! /usr/bin/env python3

# Beispiel einer typischen IoT-Device-Anwendung mit Python.
# Wie so oft lesen wir hier Temperatur und Luftfeuchtigkeit
# mit einem DHT11-Sensor aus. Die Anwendung zeigt aber, wie
# eine echte IoT-Anwendung strukturiert sein kann und bietet
# deshalb folgende Extras:
#
#  * Die Anwendung ist modular aufgebaut (Publish/Subscribe bzw. Observer-Pattern)
#  * Die gemessenen Werte können über eine HTTP REST-Schnittstelle ausgelesen werden
#  * Die gemessenen Werte werden in einer SQLite-Datenbank lokal gespeichert
#  * Eine blinkende LED zeigt an, wenn gerade eine Messung läuft
#  * Messungen können mit einem Hardware-Taster manuell gestartet werden
#  * Messungen werden alle 30 Sekunden automatisch gestartet

import time

from my_iot_device.airsensor import AirSensorHandler
from my_iot_device.button import ButtonHandler
from my_iot_device.logger import ConsoleLogHandler
from my_iot_device.database import DatabaseHandler
from my_iot_device.pubsub import PublishSubscribeBroker
from my_iot_device.restserver import RestServerHandler
from my_iot_device.statusled import StatusLedHandler

if __name__ == "__main__":
    broker = PublishSubscribeBroker()
    handlers = []
    
    handlers.append(ConsoleLogHandler(broker))     # Konsolenausgabe
    handlers.append(AirSensorHandler(broker))      # Luftsensor
    handlers.append(ButtonHandler(broker))         # Hardwarebutton
    handlers.append(StatusLedHandler(broker))      # Status-LED
    handlers.append(DatabaseHandler(broker))       # Lokale Datenbank
    handlers.append(RestServerHandler(broker))     # Lokaler HTTP-REST-Server
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        pass
    
    for handler in handlers:
        if hasattr(handler, "close"):
            handler.close()
    
    print("Bye!")