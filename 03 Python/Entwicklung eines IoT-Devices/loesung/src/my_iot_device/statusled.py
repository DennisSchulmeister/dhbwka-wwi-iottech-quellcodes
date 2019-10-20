import RPi.GPIO as GPIO 

LED_GPIO = 18
LED_FREQ = 2
LED_DUTY = 50

class StatusLedHandler:
    """
    Subscriber-Klasse für die Status-LED. Lässt die LED blinken, so lange
    eine Messung läuft.
    """
    
    def __init__(self, broker):
        """
        Konstruktor.
        
        @param broker: Zentraler PublishSubscribeBroker der Anwendung
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_GPIO, GPIO.OUT)
        self._pwm = GPIO.PWM(LED_GPIO, LED_FREQ)
        
        self._broker = broker
        self._broker.subscribe("air-sensor/status", self._air_sensor_status_cb)

    def close(self):
        """
        Aufräumarbeiten bei Programmende.
        """
        GPIO.cleanup(LED_GPIO)
        
    def _air_sensor_status_cb(self, status):
        """
        Subscriber für das Topic "air-sensor/status".
        """
        if status == "reading":
            self._pwm.start(LED_DUTY)
        else:
            self._pwm.start(0)