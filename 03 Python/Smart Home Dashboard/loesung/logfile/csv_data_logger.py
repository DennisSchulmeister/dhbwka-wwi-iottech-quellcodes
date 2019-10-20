import csv, os
from datetime import datetime
from .data_logger import DataLogger

class CSVDataLogger(DataLogger):
    """
    Ein einfacher Datenlogger, der die gemessenen Werte in einer immer
    länger werdenden CSV-Datei fortschreibt.
    """

    def __init__(self, filename):
        """
        Konstruktor.
        """
        self.filename = filename

    def log_values(self, temperature, humidity, light_switch):
        """
        Hier werden die übergebenen Messwerte in die CSV-Datei geschrieben.
        Die Datei wird hierfür geöffnet und nach dem Schreiben sofort wieder
        geschlossen, um bei einem möglichen Stromausfall nicht so viele Daten
        zu verlieren. Fehlt die Datei, wird sie neu angelegt.
        """
        write_heading = False
        
        if not os.path.exists(self.filename):
            write_heading = True
        
        with open(self.filename, "a") as file:
            writer = csv.writer(file)
            
            if write_heading:
                writer.writerow(["Zeit", "Temperatur", "Luftfeuchtigkeit", "Licht"])
            
            writer.writerow([
                datetime.now(), temperature, humidity,
                "An" if light_switch else "Aus",
            ])