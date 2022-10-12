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
Minimalbeispiel einer mit Pulsweitenmodulation zum Blinken gebrachten LED.
Die LED muss hierzu über einen Widerstand mit GPIO 12 verbunden werden.
"""

import time
import RPi.GPIO as GPIO

GPIO_LED = 12
FREQUENCY = 1       # 1 Hz
DUTY_CYCLE = 50     # 50% => 0.5 Hz

if __name__ == "__main__":
    try:
        # GPIO-Pin initialisieren
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_LED, GPIO.OUT)
        led_pwm = GPIO.PWM(GPIO_LED, FREQUENCY)
        led_pwm.start(DUTY_CYCLE)

        # Endlosschleife, damit das Programm nicht beendet wird
        while True:
            time.sleep(10)

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
