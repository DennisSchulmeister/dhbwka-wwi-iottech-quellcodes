#! ./env/bin/python3
#encoding=iso-8859-1

# Copyright Â(C) 2019 Dennis Schulmeister-Zimolong
#
# E-Mail: dhbw@windows3.de
# Webseite: https://www.wpvs.de
#
# Dieser QÃuellcode ist lizenziert unter einer
# Creative Commons Namensnennung 4.0 International Lizenz

"""
LED-Laufschrift auf der 4x64 LED-Matrix von AZ-Delivery. Die LED-Matrix
scrollt permanent die Meldung "Hallo, Raspberry Pi!" von rechts nach
links. Über einen Hardwaretaster kann die Laufschrift dabei angehalten
und wieder gestartet werden.

Die Bauteile sind hierfür wie folgt mit dem Raspberry Pi zu verbinden.
Oben rechts meint dabei den Pin, der ganz oben am Rand der Platine
direkt neben den USB-Buchen ist. Unten rechts meint entsprechend denselben
Pin in der Reihe darunter merh zur Mitte der Platine hin. Oben links ist
dann der Pin, der am nächsten zur Ecke der Platine liegt.

  +============+================+=====================================+
  | LED-Matrix | Raspi GPIO-Pin | Pin-Position                        |
  +============+================+=====================================+
  | CS         | GPIO 8         | Obere Reihe, 9ter von rechts        |
  +------------+----------------+-------------------------------------+
  | DIN        | GPIO 10        | Untere Reihe, 10ter von links       |
  +------------+----------------+-------------------------------------+
  | CLK        | GPIO 11        | Untere Reihe, 9er von rechts        |
  +------------+----------------+-------------------------------------+
  | VCC        | 5V             | Obere Reihe, 1er oder 2er von links |
  +------------+----------------+-------------------------------------+
  | GND        | Ground         | Obere Reihe, 3er von links          |
  +============+================+=====================================+

Der Taster muss so angeschlossen werden, dass er bei Betätigung GPIO 12
(obere Reihe, 5er von rechts) mit Ground verbindet. Optional kann dabei
noch ein 10 µF Kondenstor parallel und ein 1k Ohm Widerstand in Reihe
(zwischen Taster und Pi) geschaltet werden, um den Taster zu entprellen.

Diese Version der LED-Laufschrift nutzt die Python-Bibliothek Luma.LED_Matrix
zur Ansteuerung des in der LED-Matrix verbauten MAX7219 Chips, der via SPI
(Serial Peripherial Interface) mit dem Raspberry Pi kommuniziert. Aus diesem
Grund muss sichergestellt sein, dass die SPI-Kernelmodule geladen sind, bevor
das Programm gestartet wird.
"""

import os, time
import RPi.GPIO as GPIO

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from PIL import ImageFont

GPIO_BUTTON = 12
AMOUNT_PANELS = 4
PANEL_WIDTH = 8
PANEL_HEIGHT = 8
MESSAGE="Hallo, Raspberry Pi!"

if __name__ == "__main__":
    try:
        # GPIO-Pin für den Taster initialisieren
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(GPIO_BUTTON, GPIO.RISING, bouncetime=400)

        # LED-Matrix initialisieren
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial, cascaded=AMOUNT_PANELS, block_orientation=-90)
        virtual = viewport(device, width=200, height=100)

        srcdir = os.path.dirname(os.path.realpath(__file__))
        small_font = ImageFont.truetype(os.path.join(srcdir, "pixelmix", "pixelmix.ttf"), PANEL_HEIGHT)

        with canvas(virtual) as draw:
            draw.text((AMOUNT_PANELS * PANEL_WIDTH, 0), MESSAGE, fill="white", font=small_font)
            text_width = draw.textsize(MESSAGE, font=small_font)[0]

        max_offset = text_width + (AMOUNT_PANELS * PANEL_WIDTH)
        offset = 0
        running = True

        while True:
            time.sleep(0.1)

            # Taster zum Anhalten/Fortsetzen der Laufschrift abfragen
            if GPIO.event_detected(GPIO_BUTTON):
                print("%s: Tasten Event" % time.strftime("%d.%m.%Y %H:%M:%S"))
                if running:
                    running = False
                else:
                    running = True

            # Scrollposition der Laufschrift aktualisieren
            if running:
                virtual.set_position((offset, 0))
                offset += 1

                if offset > max_offset:
                    offset = 0
    except KeyboardInterrupt:
        pass
