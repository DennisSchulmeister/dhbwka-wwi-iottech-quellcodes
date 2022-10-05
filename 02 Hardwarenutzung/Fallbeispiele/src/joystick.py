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
Beispiel zum Auslesen des KY-023 Joysticks mit dem KY-053 A/D-Wandler.
"""

import curses
import time
import busio
import adafruit_ads1x15.ads1115 as ADC
from adafruit_ads1x15.analog_in import AnalogIn

ADC_CLOCK = 3
ADC_SDATA = 2

if __name__ == "__main__":
    try:
        # Terminal initialisieren
        screen = curses.initscr()

        # A/D-Konverter initialisieren
        i2c_bus = busio.I2C(ADC_CLOCK, ADC_SDATA)
        ad_converter = ADC.ADS1115(i2c_bus)
        adc_channel0 = AnalogIn(ad_converter, ADC.P0)
        adc_channel1 = AnalogIn(ad_converter, ADC.P1)

        # Endlosschleife, damit das Programm weiterläuft
        while True:
            # Achsen messen
            x_voltage = adc_channel0.voltage
            x_value = adc_channel0.value

            y_voltage = adc_channel1.voltage
            y_value = adc_channel1.value

            # Ergebnis anzeigen
            screen.clear()

            screen.addstr(0, 0, "X-ACHSE")
            screen.addstr(0, 15, "Spannung: %s V" % x_voltage)
            screen.addstr(0, 55, "Messwert: %s" % x_value)

            screen.addstr(1, 0, "Y-ACHSE")
            screen.addstr(1, 15, "Spannung: %s V" % y_voltage)
            screen.addstr(1, 55, "Messwert: %s" % y_value)

            screen.refresh()

            # Kurz warten
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    curses.endwin()
    i2c_bus.deinit()
