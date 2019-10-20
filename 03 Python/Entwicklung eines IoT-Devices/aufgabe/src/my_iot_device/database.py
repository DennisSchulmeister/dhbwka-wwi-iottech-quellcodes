import apsw, os

DBFILE = os.path.join(os.path.expanduser("~"), "my_iot_device.sqlite")

class DatabaseHandler:
    """
    Einfacher Datenbank-Handler, der die gemessenen Sensorwerte in einer
    lokelen SQLite-Datenbank ablegt. Auf diese Weise ist schon einmal
    sichergestellt, dass die Werte nicht verloren gehen. Insbesondere,
    da diese Version der Anwendung die Daten an keinen Backend-Server
    schickt. Doch selbst, wenn die Daten an einen Server geschickt werden
    würden, sollten sie lokal zwischengespeichert werden, um einen Ausfall
    der Internetverbindung zu überbrücken.
    
    Die Datenbankdatei wird im Home-Verzeichnis abgelegt.
    
    https://sqliteonline.com/ bietet eine einfache Möglichkeit, sich die
    Inhalte der Datenbank anzeigen zu lassen.
    """
    
    def __init__(self, broker):
        """
        Konstruktor.
        
        @param broker: Zentraler PublishSubscribeBroker der Anwendung
        """
        # TODO: Datenbankverbindung öffnen
        
        self._broker = broker
        # TODO: Sensorwerte empfangen

    def close(self):
        """
        Aufräumarbeiten bei Programmende.
        """
        # TODO: Datenbankverbindung schließen
