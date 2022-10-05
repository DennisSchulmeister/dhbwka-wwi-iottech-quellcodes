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
Beispiel zur Ansteuerung eines Servomotors via Pulsweitenmodulation
"""

import time
import RPi.GPIO as GPIO

MOTOR_GPIO  = 17
MOTOR_FREQ  = 50    # Frequenz: 50 Hz = 20ms
MOTOR_DUTY  = 5     # Lastzyklus 5%   = 1ms

def set_motor_position(percent):
    """
    Vgl. https://components101.com/servo-motor-basics-pinout-datasheet

    Die Position des Servomotors wird mit einem PWM-Signal gesteuert,
    das einen Zyklus von 20ms = 50 Hz haben muss. Innerhalb dieses
    Zyklus signalisiert ein Puls von 1ms (5% Lastzyklus) die Position
    ganz links und ein Puls von 2ms (10% Lastzyklus) ganz rechts.

    Das Signal muss so lange aufrecht erhalten werden, bis der Servo
    sein Position erreicht hat. Der Einfachheit halber wird hier deshalb
    einfach 0,3 Sekunden gewartet.
    """
    duty_cycle = MOTOR_DUTY * (1 + percent)
    pwm = GPIO.PWM(MOTOR_GPIO, MOTOR_FREQ)
    pwm.start(duty_cycle)
    time.sleep(.3)
    pwm.stop()

if __name__ == "__main__":
    try:
        # GPIO-Pins initialisieren
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MOTOR_GPIO, GPIO.OUT)

        # Endlosschleife
        while True:
            set_motor_position(0)
            time.sleep(1)
            set_motor_position(1)
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
