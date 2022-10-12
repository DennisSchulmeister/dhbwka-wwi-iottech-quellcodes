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
Minimalbeispiel einer blinkenden LED. Hierzu wird einfach der GPIO 21
abwechselnd ein und ausgeschaltet. Dieser kann dann entweder über einen
Widerstand direkt die LED ansteuern, oder mit Hilfe eines Transistors
oder Relais einen Laststrom schalten.
"""

import os, time
import RPi.GPIO as GPIO

GPIO_BUTTON = 20
GPIO_LED    = 21
GPIO_RELAIS = 22
BLINK_S     = 0.5
RELAIS_S    = 10

led_on      = False
relais_on   = False
timer_s     = 0


def on_button_event(button):
    """
    Button-Callback. Wird immer dann aufgerufen, wenn sich der Zustand
    des Hardware-Button Ändert.
    """
    led_on    = True
    relais_on = True
    timer_s   = 0

if __name__ == "__main__":
    try:
        # GPIO-Pins initialisieren
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO_LED, GPIO.OUT)
        GPIO.setup(GPIO_RELAIS, GPIO.OUT)

        GPIO.add_event_detect(GPIO_BUTTON, GPIO.HIGH)
        GPIO.add_event_callback(GPIO_BUTTON, on_button_event)

        # Bei Knopfdruck LED blinken und Relais anschalten
        while True:
            time.sleep(BLINK_S)

            if not relais_on:
                continue

            led_on = not led_on
            GPIO.output(GPIO_LED, led_on)
            GPIO.output(GPIO_RELAIS, relais_on)

            timer_s += BLINK_S

            if timer_s >= RELAIS_S
                led_on    = False
                relais_on = False
                timer_s   = 0

                GPIO.output(GPIO_LED, led_on)
                GPIO.output(GPIO_RELAIS, relais_on)

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
