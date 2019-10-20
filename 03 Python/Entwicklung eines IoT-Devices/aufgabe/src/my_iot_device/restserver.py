import cherrypy, threading

SERVER_PORT = 8080
MAX_COUNT = 1000

class RestServerHandler:
    """
    Handler-Klasse für einen einfachen, eingebauten Webserver. Der Webserver
    startet auf Port SERVER_PORT und liefert eine einfache JSON-Struktur
    mit MAX_COUNT Datensätzen, die seit dem Start der Anwendung gemessen
    wurden. Dies könnte nun relativ einfach zu einer AJAX-fähigen Webanwendung
    zur Steuerung des IoT-Devices ausgebaut werden.
    """
    
    def __init__(self, broker):
        """
        Konstruktor.
        
        @param broker: Zentraler PublishSubscribeBroker der Anwendung
        """
        self._data = []
        self._lock = threading.Lock()
        
        self._broker = broker
        self._broker.subscribe("air-sensor/values", self._air_sensor_values_cb)
  
        web_server_thread = threading.Thread(target=self._web_server_thread)
        web_server_thread.start()

    def close(self):
        """
        Aufräumarbeiten bei Programmende.
        """
        cherrypy.engine.exit()

    def _web_server_thread(self):
        """
        Eigener Thread zur Ausführung des Webserers, da die Methode
        cherrypy.quickstart() den rufenden Thread blockiert, während
        der Server läuft. 
        """
        cherrypy.config.update({
            "log.screen": False,
            "log.access_file": "",
            "log.error_file": "",
            "server.socket_port": SERVER_PORT,
            "tools.gzip.on": True,
        })
        
        cherrypy.quickstart(self, "/")

    def _air_sensor_values_cb(self, time, h, t):
        """
        Subscriber für das Topic "air-sensor/values". Legt die empfangenen
        Werte (seit dem die Anwendung läuft) in self._data ab. Die maximale
        Anzahl der Datensätze wird dabei auf MAX_COUNT reduziert, damit die
        Anwendung bei Dauerbetrieb nicht irgendwann wegen Speichermangel
        abstürzt. :-)
        """
        self._lock.acquire()
        
        self._data.append({
            "time": str(time),
            "temp": t,
            "humidity": h,
        })
        
        self._data = self._data[-MAX_COUNT:]
        
        self._lock.release()
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        self._lock.acquire()
        data = self._data.copy()
        self._lock.release()
        
        return data