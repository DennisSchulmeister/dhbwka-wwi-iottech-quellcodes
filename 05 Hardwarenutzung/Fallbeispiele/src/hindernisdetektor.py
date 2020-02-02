#! ./env/bin/python3
#encoding=utf-8

# Copyright (C) 2020 Dennis Schulmeister-Zimolong
#
# E-Mail: dhbw@windows3.de
# Webseite: https://www.wpvs.de
#
# Diese Quellcode ist lizenziert unter einer
# Creative Commons Namensnennung 4.0 International Lizenz

"""
Beispiel zur Ansteuerung des KY-032 Hindernisdetektors und der KY-011 2-Farb LED
aus dem X40 Sensorkit. Erkennt der Detetkor kein Hindernis, leuchtet die LED grün,
andernfalls rot.
"""

import time
import RPi.GPIO as GPIO

DETECTOR_GPIO  = 11
LED_GREEN_GPIO = 24
LED_RED_GPIO   = 23

def on_detector_change(*args, **kwargs):
    """
    Callback-Funktion, die bei jeder Änderung des Hindernisdetektors
    aufgerufen wird. Hier wird die 2-Farb LED in Abhängigkeit des
    erkannten Ereignisses an oder ausgeschaltet.
    """
    obstacle_detected = GPIO.input(DETECTOR_GPIO)

    print ("Hindernis erkannt: %s" % (not obstacle_detected))

    GPIO.output(LED_GREEN_GPIO, not obstacle_detected)
    GPIO.output(LED_RED_GPIO, obstacle_detected)

if __name__ == "__main__":
    try:
        # GPIO-Pins initialisieren
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DETECTOR_GPIO, GPIO.IN)
        GPIO.setup(LED_RED_GPIO, GPIO.OUT)
        GPIO.setup(LED_GREEN_GPIO, GPIO.OUT)

        GPIO.add_event_detect(DETECTOR_GPIO, GPIO.BOTH, bouncetime=15)
        GPIO.add_event_callback(DETECTOR_GPIO, on_detector_change)
        on_detector_change()

        # Endlosschleife, damit das Programm weiterläuft
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
