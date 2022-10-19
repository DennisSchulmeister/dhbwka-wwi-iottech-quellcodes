#! /bin/env python3
#encoding=utf-8

# Copyright (C) 2019 Dennis Schulmeister-Zimolong
#
# E-Mail: dhbw@windows3.de
# Webseite: https://www.wpvs.de
#
# Dieser Quellcode ist lizenziert unter einer
# Creative Commons Namensnennung 4.0 International Lizenz

"""
Beispiel zum Auslesen eines DHT11-Sensors via 1-wire. Die Datenleitung des
Sensors muss hierzu mit GPIO 23 verbunden werden. Zusätzlich muss der Sensor
über seine anderen beiden Leitungen mit Strom versorgt werden.
"""
import os, time
import Adafruit_DHT

GPIO_SENSOR = 4
DELAY_S = 2

if __name__ == "__main__":
    try:
        # Sensor initialisieren
        dht_sensor = Adafruit_DHT.DHT11

        # Alle 2 Sekunden eine Messung vornehmen
        while True:
            time.sleep(DELAY_S)

            print("Beginne mit der Messung")
            h, t = Adafruit_DHT.read_retry(dht_sensor, GPIO_SENSOR)

            if h == None and t == None:
                print("Fehler bei der Messung")
            else:
                print("Temperatur: %s Grad Celsius, Rel. Luftfeuchtigkeit: %s" % (t,h))

            print("")

    except KeyboardInterrupt:
        pass
