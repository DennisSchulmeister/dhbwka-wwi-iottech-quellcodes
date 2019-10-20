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
        self._connection = apsw.Connection(DBFILE)
        self._cursor = self._connection.cursor()
        self._cursor.execute("CREATE TABLE IF NOT EXISTS airsensor(time, temp, humidity)")
        
        self._broker = broker
        self._broker.subscribe("air-sensor/values", self._air_sensor_values_cb)

    def close(self):
        """
        Aufräumarbeiten bei Programmende.
        """
        self._connection.close()

    def _air_sensor_values_cb(self, time, h, t):
        """
        Subscriber für das Topic "air-sensor/values".
        """
        values = {
            "time": str(time),
            "temp": t,
            "humidity": h, 
        }
        
        self._broker.publish("database/status", "writing")
        self._cursor.execute("INSERT INTO airsensor VALUES(:time, :temp, :humidity)", values)
        self._broker.publish("database/status", "finished")
