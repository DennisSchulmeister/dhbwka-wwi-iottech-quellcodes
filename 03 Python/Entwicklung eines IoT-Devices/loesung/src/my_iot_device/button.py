import RPi.GPIO as GPIO

BUTTON_GPIO = 21

class ButtonHandler:
    """
    Publisher-Klasse für den Hardwarebutton. Setzt eine Callback-Methode auf,
    die darauf wartet, dass der Button gedrückt wird und dann eine Nachricht
    an den Luftsensor schickt, um eine neue Messung anzustoßen.
    """
    
    def __init__(self, broker):
        """
        Konstruktor.
        
        @param broker: Zentraler PublishSubscribeBroker der Anwendung
        """
        self._broker = broker

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, bouncetime=20)
        GPIO.add_event_callback(BUTTON_GPIO, self._button_pushed_cb)

    def close(self):
        """
        Aufräumarbeiten bei Programmende.
        """
        GPIO.cleanup(BUTTON_GPIO)

    def _button_pushed_cb(self, button):
        """
        Callback-Funktion für den Hardwarebutton. Wird automatisch aufgerufen,
        sobald der Button runteredrückt und wieder losgelassen wird. Sendet
        eine Nachricht an das Topic "air-sensor/command", um einen neuen
        Lesevorgang zu starten.
        """
        self._broker.publish("air-sensor/command", "read")