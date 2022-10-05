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
Minimalbeispiel einer helligkeitsgesteuerten LED. Die LED wird hierzu über
einen Widerstand mit GPIO 12 verbunden, der mit Pulsweitenmodulation die
Helligkeit der LED beeinflusst.
"""

import time
import RPi.GPIO as GPIO

GPIO_LED = 12
FREQUENCY = 50
DELAY_S = 0.2

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
            print("Duty Cycle: %s" % duty_cycle)
            led_pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(DELAY_S)

            if go_up:
                duty_cycle += 10
            else:
                duty_cycle -= 10

            if duty_cycle >= 100:
                go_up = False
                print("")
            elif duty_cycle <= 0:
                go_up = True
                print("")


    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
