import Adafruit_DHT, datetime, random, threading, time
from threading import Lock

AUTO_READ_DELAY_SEC = 30

SENSOR_DELAY_SEC = 2
SENSOR_TYPE = Adafruit_DHT.DHT11
SENSOR_GPIO = 23

class AirSensorHandler:
    """
    Handler-Klasse für den Luftsensor. Reagiert auf das Topic "air-sensor/command"
    und den Wert "read", um eine neue Messung zu starten. Gleichzeitig wird ein
    Hintergrundthread gestartet, der alle AUTO_READ_DELAY_SEC Sekunden an das Topic
    schreibt, um automatisch eine Messung anzustoßen.
    
    Die Messung wird über folgende Topics kommuniziert:
    
    "air-sensor/status" = "reading"
    "air-sensor/status" = "finished"
    "air-sensor/values" = {t: 0.0, h: 0.0)
    """
    
    def __init__(self, broker):
        """
        Konstruktor.
        
        @param broker: Zentraler PublishSubscribeBroker der Anwendung
        """
        self._lock = Lock()
        
        self._broker = broker
        self._broker.subscribe("air-sensor/command", self._air_sensor_command_cb)
        
        self._trigger_thread_flag_quit = threading.Event()
        self._trigger_thread = threading.Thread(target=self._trigger_automatic_read_thread, daemon=True)
        self._trigger_thread.start()

    def close(self):
        """
        Aufräumarbeiten bei Programmende.
        """
        # Trigger-Thread beenden
        self._trigger_thread_flag_quit.set()
    
    def _trigger_automatic_read_thread(self):
        """
        Thread, der automatisch alle AUTO_READ_DELAY_SEC Sekunden eine Nachricht
        an das Topic "air-sensor/command" schickt, um einen neuen Lesevorgang
        zu starten. Läuft als Daemon-Thread im Hintergrund und wird daher bei
        Programmende automatisch gestoppt.
        """
        while True:
            self._broker.publish("air-sensor/command", "read")
            
            if self._trigger_thread_flag_quit.wait(AUTO_READ_DELAY_SEC):
                break
            
    def _air_sensor_command_cb(self, command):
        """
        Subscriber für das Topic "air-sensor/command". Hier wird auf das "read"-Kommando
        reagiert, um eine neue Messung zu starten. Die Messung unterbricht den rufenden
        Thread für SENSOR_DELAY_SEC Sekunden, damit sich die Messwerte des Sensors in dieser
        Zeit stabilisieren.
        
        Beginn und Ende der Messung werden über das Topic "air-sensor/status" mit den
        beiden Werten "reading" und "finished" bekannt gegeben. Der gemessene Wert wird
        daraufhin an das Topic "air-sensor/values" als **kwargs{"time": xxx, "t": 0.0, "h": 0.0}
        gesendet.
        """
        if not command == "read" \
        or not self._lock.acquire(blocking=False):
            return
        
        self._broker.publish("air-sensor/status", "reading")
        
        h = None
        t = None
        
        while h == None or t == None:
            time.sleep(SENSOR_DELAY_SEC)
            #h, t = Adafruit_DHT.read_retry(SENSOR_TYPE, SENSOR_GPIO)
            h = random.randint(0, 500) / 10.0
            t = random.randint(0, 350) / 10.0
        
        h = round(h, 1)
        t = round(t, 1)
        now = datetime.datetime.now()
        
        self._broker.publish("air-sensor/status", "finished")
        self._broker.publish("air-sensor/values", time=now, t=t, h=h)
        self._lock.release()