#! /usr/bin/env python3

# Beispiel für die Gliederung des Quellcodes eíner in Python geschriebenen Anwendung
# zur Ansteuerung von externen Hardwarekomponenten. Die Anwendung realisiert dabei
# eine einfache Einparkhilfe, auf Knopfdruck beginnt, mit einem Ultraschallsensor so
# lange den Abstand zu messen, bis der Knopf erneut gedrükt wird. Eine zweifarbige
# LED sowie ein Buzzer informieren über den gemessenen Abstand. Zusätzlich wird der
# gemessene Wert in Echtzeit in einer kleinen Benutzeroberfläche dargestellt.

import time

from myapp.gui.console_logger import ConsoleLogger
from myapp.gui.main_window import MainWindow
from myapp.hardware.distance_sensor import DistanceSensor
from myapp.hardware.led_beeper import LedBeeper
from myapp.hardware.trigger_button import TriggerButton
from myapp.utils.observable import Observable

if __name__ == "__main__":
    event_broker = Observable(use_event_thread=True)
    
    handlers = [
        # Konsolenausgabe
        ConsoleLogger(event_broker),
        
        # Hauptfenster
        MainWindow(event_broker),
        
        # Ein/Aus-Knopf
        TriggerButton(event_broker, gpio_pin=23),
        
        # Ultraschallsensor
        DistanceSensor(event_broker, gpio_pin_trigger=10, gpio_pin_echo=9),
        
        # LED un Piepser
        LedBeeper(event_broker, gpio_pin_led=7, gpio_pin_beeper=13,
                  distance_cm_min=10, distance_cm_max=50,
                  frequency_hz_min=10, frequency_hz_max=1)
    ]
    
    print("Drücken Sie Strg+C zum Beenden")
    
    try:
        event_broker.join_thread()
    except KeyboardInterrupt:
        event_broker.raise_event("quit")
        event_broker.close()
        event_broker.join_thread()

    print("Bye!")