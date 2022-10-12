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
Minimalbeispiel zum Auslesen eines Hardware-Buttons, der mit einen
EXTERNEN Pull-Down-Widerstand verbunden ist. Durch den Pull-Down wird
der GPIO-Eingangspin mit Masse (deshalb Pull-DOWN) verbunden. Der Button
zieht den Pin dann auf 3,3V hoch, wenn er gedrückt wird. Im Beispiel
wird dazu GPIO 22 verwendet.

An GPIO 21 kann eine Kontroll-LED angeschlossen werden, die immer dann
leuchtet, solange der Button gedrückt ist.
"""

import time
import RPi.GPIO as GPIO

GPIO_BUTTON = 22
GPIO_LED = 21

def on_button_event(button):
    """
    Button-Callback. Wird immer dann aufgerufen, wenn sich der Zustand
    des Hardware-Button Ändert.
    """
    if GPIO.input(button) == GPIO.HIGH:
        print("Der Button ist UNTEN / AN")
        GPIO.output(GPIO_LED, True)
    else:
        print("Der Button ist OBEN / AUS")
        print("")
        GPIO.output(GPIO_LED, False)

if __name__ == "__main__":
    try:
        # GPIO-Pins initialisieren
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_BUTTON, GPIO.IN)
        GPIO.setup(GPIO_LED, GPIO.OUT)

        GPIO.add_event_detect(GPIO_BUTTON, GPIO.BOTH)
        GPIO.add_event_callback(GPIO_BUTTON, on_button_event)

        # Endlosschleife, damit das Hauptprogramm weiterläuft
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
