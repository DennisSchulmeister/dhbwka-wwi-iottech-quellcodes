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
Beispiel zur Ansteuerung eines LCD-Displays via SPI. Da das Display ein
relativ komplexes Protokoll hat, befindet sich die eigentliche, serielle
Kommunikation in der ST7735-Bibliothek von Adafruit.
"""

import time
import ST7735 as TFT
from PIL import Image

TFT_WIDTH = 128
TFT_HEIGHT = 160
TFT_FREQUENCY = 4000000

TFT_GPIO_DC = 24
TFT_GPIO_RESET = 25
TFT_SPI_PORT = 0
TFT_SPI_DEVICE = 0

if __name__ == "__main__":
    try:
        # Display initialisieren
        tft = TFT.ST7735(
            port   = TFT_SPI_PORT,
            cs     = TFT_SPI_DEVICE,
            dc     = TFT_GPIO_DC,
            rst    = TFT_GPIO_RESET,
            width  = TFT_WIDTH,
            height = TFT_HEIGHT
        )

        tft.begin()
        tft.clear()

        # Bild auf dem Display anzeigen
        image = Image.open(os.path.join(os.path.dirname(__file__), "dog.jpg"))
        image = image.resize((TFT_WIDTH, TFT_HEIGHT))

        tft.display(image)

        # Endlosschleife, damit das Programm nicht beendet wird
        while True:
            time.sleep(10)

    except KeyboardInterrupt:
        pass

    tft.clear()
