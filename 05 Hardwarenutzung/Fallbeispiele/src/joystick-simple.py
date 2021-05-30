#! ./env/bin/python3
#encoding=utf-8

# Copyright (C) 2021 Dennis Schulmeister-Zimolong
#
# E-Mail: dhbw@windows3.de
# Webseite: https://www.wpvs.de
#
# Diese Quellcode ist lizenziert unter einer
# Creative Commons Namensnennung 4.0 International Lizenz

"""
---------------------------------------------------------------------------
Mini-Beispiel zum Auslesen des Joysticks mit dem A/D-Wandler des Sensorkits
---------------------------------------------------------------------------

Wie sich herausgestellt hat, ist die Dokumentation des Sensorkits an dieser
Stelle leider veraltet. Zum einen weil es noch Python 2.x Syntax enthält,
andererseits aber auch, weil die verwendete Adafruit-Bibliothek nicht mehr
weiterentwickelt wird. Die Bibliothek Adafruit-ADS1x15 aus dem Beispiel
wurde durch adafruit-circuitpython-ads1x15 ersetzt, die zwar leistungsfähiger
dafür aber auch aufwändiger in der Nutzung ist. In PyPi gibt es mit ADS1x15-ADC
aber eine sehr einfache Bibliothek, die genau das macht, was wir wollen.

Hier eine kleine Schritt-für-Schritt-Anleitung, um das Beispielprogramm
zum Laufen zu bringen. Alle Befehle sind auf der Konsole auszuführen:

  1. I²C-Port in raspi-config aktivieren:

     $ sudo raspi-config

  2. Neues Python-Environment erzeugen, falls noch nicht geschehen:

     $ python3 -m venv env
     $ . env/bin/activate

  3. Bibliothek ADS1x15-ADC installieren:

     $ pip install ADS1x15-ADC

     Besser kann der Name der Bibliothek in eine Datei namens
     requirements.txt geschrieben und diese dann installiert werden:

     $ pip install -r requirements.txt

  4. Beispiel ausführen:

     $ python3 joystick.py

Die Hardware muss hierfür wie folgt verkabelt sein:

  Joystick[GND]    --> Raspi[GND]
  Joystick[+5V]    --> Raspi[+5V]
  Joystick[VRy]    --> A/D-Wandler[A0]

  A/D-Wandler[GND] --> Raspi[GND]
  A/D-Wandler[VDD] --> Raspi[+5V]
  A/D-Wandler[SCL] --> Raspi[Pin 5: SCL]
  A/D-Wandler[SDA] --> Raspi[Pin 3: SDA]

Für eine Skizze, wo sich die Pins 3 und 5 des Pi befinden siehe
die zweite Grafik auf https://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/

Die Pins sind direkt im Eck unter dem +3.3V-Pin.
"""

import time
import ADS1x15

if __name__ == "__main__":
    ads = ADS1x15.ADS1115(1)

    ads.setInput(7)
    ads.setGain(1)
    ads.setMode(1)
    ads.setDataRate(7)

    try:
        while True:
            time.sleep(1)

            value = ads.readADC(0)
            voltage = ads.toVoltage(value)

            print(f"Raw ADC: {value}\tVoltage: {voltage} V")
    except KeyboardInterrupt:
        pass
