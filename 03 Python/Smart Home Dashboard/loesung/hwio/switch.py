import time
import RPi.GPIO as GPIO
from .hwdevice import HardwareDevice

class SwitchOutputDevice(HardwareDevice):
    """
    Klasse zur Ansteuerung eines einfachen, binären GPIO-Ausgangs. Der Ausgang
    kann dazu genutzt werden, eine LED oder irgend eine andere Last (z.B. ein
    Relais) ein oder auszuschalten. Zusätzlich kann der Ausgang in regelmäßigen
    Abständen automatisch ein- und ausgeschaltet werden, um z.B. eine LED zum
    Blinken zu bringen.
    """
    
    STATE_OFF   = 0
    STATE_ON    = 1
    STATE_BLINK = 2
    
    def __init__(self, gpio_pin):
        """
        Konstruktor.
        
        @param gpio_pin: PIN-Nummer der LED
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.OUT)
        
        self._gpio_pin = gpio_pin
        self._state = self.STATE_OFF
        self._blink_sec = 0
        self._last_blink = 0
        self._blink_on = False
        self._need_update = False
    
    def switch_on(self, on):
        """
        Schaltet den Ausgang ein- oder aus.
        @param on: True, wenn der Ausgang eingeschaltet werden soll
        """
        self._need_update = True
        
        if on:
            self._state = self.STATE_ON
        else:
            self._state = self.STATE_OFF
    
    def blink(self, blink_sec):
        """
        Schaltet den Ausgang periodisch ein oder aus.
        @param blink_sec: Anzahl Sekunden zwischen den Schaltvorgängen
        """
        self._state = self.STATE_BLINK
        self.blink_sec = blink_sec
        self._last_blink = 0

    def tick(self):
        """
        Hauptmethode, in welcher der Ausgang tatsächlich geschaltet wird.
        """
        if self._state == self.STATE_ON and self._need_update:
            self._output(True)
        elif self._state == self.STATE_OFF and self._need_update:
            self._output(False)
        elif self._state == self.STATE_BLINK:
            now = time.perf_counter()
            elapsed_sec = now - self._last_blink
            
            if elapsed_sec >= self._blink_sec:
                self._last_blink = now
                self._blink_on = not self._blink_on
                self._output(self._blink_on)
        
        self._need_update = False
                
    def close(self):
        """
        Beenden des Hardwarezugriffs.
        """
        self._state = self.STATE_OFF
        self._output(False)

    def _output(self, value):
        """
        Hilfsmethode zum Ein- oder Ausschalten des GPIO-Ausgangs. Hier wird
        der Schaltvorgang zusätzlich noch in der Konsole protokolliert.
        """
        value_text = "An" if value else "Aus"
        print("GPIO %s: %s" % (self._gpio_pin, value_text))
        
        GPIO.output(self._gpio_pin, value)