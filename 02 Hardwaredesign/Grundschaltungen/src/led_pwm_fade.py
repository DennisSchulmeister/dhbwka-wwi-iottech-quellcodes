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
Minimalbeispiel einer helligkeitsgesteuerten LED. Die LED wird hierzu mit
GPIO 12 verbunden, der mit einem PWM-Signal (Pulsweitenmodulation) die
Helligkeit der LED beeinflusst.
"""

import os, time
import RPi.GPIO as GPIO

GPIO_LED = 12
FREQUENCY = 50
DELAY_S = 0.01
DELTA = 1.25

if __name__ == "__main__":
    try:
        # GPIO-Pin initialisieren
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_LED, GPIO.OUT)
        led_pwm = GPIO.PWM(GPIO_LED, FREQUENCY)

        # LED alle 0.2 Sekunden heller / dunkler machen
        duty_cycle = 0
        go_up = True

        led_pwm.start(duty_cycle)

        while True:
            if duty_cycle >= 100:
                go_up = False
                print("LED abdunkeln -")
            elif duty_cycle <= 0:
                go_up = True
                print("LED aufhellen +")

            if go_up:
                duty_cycle += DELTA
            else:
                duty_cycle -= DELTA

            led_pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(DELAY_S)

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
