import RPi.GPIO as GPIO

class TriggerButton:
    """
    Handler-Klasse für den Hardwarebutton. Setzt eine Callback-Methode auf,
    die darauf wartet, dass der Button gedrückt wird und dann ein Ereignis
    auslöst, um entweder eine neue Messung zu starten oder eine laufende
    Messen zu beenden.
    
    Reagiert auf folgende Ereignisse:
    
      * keine

    Löst folgende Ereignisse aus:
    
      * command(name="trigger-measurement")
    """
    
    def __init__(self, event_broker, gpio_pin):
        """
        Konstruktor.
        
        @param event_broker: Zentraler Event Broker der Anwendung
        @param gpio_pin: GPIO-Nummer des Buttons
        """
        self._event_broker = event_broker
        self._gpio_pin = gpio_pin
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(gpio_pin, GPIO.FALLING, bouncetime=20)
        GPIO.add_event_callback(gpio_pin, self._on_button_pushed)
        
        event_broker.add_event_listener("quit", self._on_quit)

    def _on_quit(self):
        """
        Aufräumarbeiten bei Programmende.
        """
        GPIO.cleanup(self._gpio_pin)

    def _on_button_pushed(self, button):
        """
        Callback-Funktion für den Hardwarebutton. Wird automatisch aufgerufen,
        sobald der Button gedrückt und wieder losgelassen wird. Löst das Ereignis
        `command(name="trigger-measurement")` aus, um eine Messung zu starten oder
        zu stoppen.
        """
        self._event_broker.raise_event("command", name="trigger-measurement")
