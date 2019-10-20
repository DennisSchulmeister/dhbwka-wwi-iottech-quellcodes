import random, time
import Adafruit_DHT
from .hwdevice import HardwareDevice

class DHT11Sensor(HardwareDevice):
    """
    Simple Implementierung für den Zugriff auf einen DHT11-Luftsensor via
    1-wire. Die Klasse kapselt im Grunde genommen einfach nur die Bibliothek
    Adafruit_DHT und ermöglicht es dabei, sich in regelmäßigen Abständen neue
    Werte auszulesen.
    """
    
    def __init__(self, gpio_pin, interval_sec, read_cb=None):
        """
        Konstrutor.
        
        @param gpio_pin:     PIN-Nummer des Sensors
        @param interval_sec: Interval, in dem die Daten gelesen werden
        @param read_cb:      Rückruffunktion für neue Daten
        
        Die Callback-Funktion muss folgende Signatur haben:
        
        def dht11_read_cb(temperature, humidity):
            …
        """
        self._sensor = Adafruit_DHT.DHT11
        self._gpio_pin = gpio_pin
        self._interval_sec = interval_sec
        self._read_cb = read_cb
        self._last_read = 0
    
    def tick(self):
        """
        Hauptmethode, in welcher die Sensordaten gelesen werden.
        """
        now = time.perf_counter()
        elapsed_sec = now - self._last_read
            
        if elapsed_sec >= self._interval_sec and self._read_cb:
            humidity, temperature = Adafruit_DHT.read_retry(self._sensor, self._gpio_pin)
            
            temperature = round(temperature, 1)
            humidity = round(humidity, 1)
            
            self._read_cb(temperature, humidity)

    def close(self):
        """
        Hardwarezugriff beenden. Wird hier nicht benötigt, muss aber überschrieben
        werden, da es eine abstrakte Methode ist.
        """
        pass

class DHT11MockSensor(HardwareDevice):
    """
    Mockklasse zum Simulieren eines DHT11-Luftsensors, wenn man gerade keinen
    eigenen zur Hand hat. Die Klasse simuliert einfach irgendwelche Veränderungen
    ausgehend von einem Zufallswert zwischen 10 und 35 für beide Werte.
    """
    
    def __init__(self, interval_sec, read_cb=None):
        """
        Konstrutor.
        
        @param interval_sec: Interval, in dem die Daten gelesen werden
        @param read_cb:      Rückruffunktion für neue Daten
        
        Die Callback-Funktion muss folgende Signatur haben:
        
        def dht11_read_cb(temperature, humidity):
            …
        """
        self._interval_sec = interval_sec
        self._read_cb = read_cb
        self._last_read = 0
        
        self._temperature = random.randint(10, 35)
        self._humidity = random.randint(10, 35)
    
    def tick(self):
        """
        Hauptmethode, in welcher die Sensordaten gelesen werden.
        """
        now = time.perf_counter()
        elapsed_sec = now - self._last_read
            
        if elapsed_sec >= self._interval_sec and self._read_cb:
            self._last_read = now
            
            self._temperature += random.randint(-15, 15) / 10.0
            self._humidity += random.randint(-15, 15) / 10.0
            
            self._temperature = max(min(round(self._temperature, 1), 40.0), 0.0)
            self._humidity = max(min(round(self._humidity, 1), 40.0), 0.0)
            
            self._read_cb(self._temperature, self._humidity)

    def close(self):
        """
        Hardwarezugriff beenden. Wird hier nicht benötigt, muss aber überschrieben
        werden, da es eine abstrakte Methode ist.
        """
        pass