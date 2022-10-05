#! ./env/bin/python3
#encoding=utf-8

# Copyright (C) 2019 Dennis Schulmeister-Zimolong
#
# E-Mail: dhbw@windows3.de
# Webseite: https://www.wpvs.de
#
# Dieser Quellcode ist lizenziert unter einer
# Creative Commons Namensnennung 4.0 International Lizenz

"""
Minimalbeispiel einer blinkenden LED. Hierzu wird einfach der GPIO 21
abwechselnd ein und ausgeschaltet. Dieser kann dann entweder über einen
Widerstand direkt die LED ansteuern, oder mit Hilfe eines Transistors
oder Relais einen Laststrom schalten.
"""

import os, time
import RPi.GPIO as GPIO

GPIO_LED = 21
DELAY_S = 0.5

if __name__ == "__main__":
    try:
        # GPIO-Pin initialisieren
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_LED, GPIO.OUT)

        # LED alle halbe Sekunde ein bzw. ausschalten
        led_status = False

        while True:
            led_status = not led_status
            GPIO.output(GPIO_LED, led_status)

            print("LED ist an" if led_status else "LED ist aus")

            time.sleep(DELAY_S)
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
