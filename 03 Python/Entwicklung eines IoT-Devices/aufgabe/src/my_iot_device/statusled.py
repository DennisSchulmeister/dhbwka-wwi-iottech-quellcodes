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
        self._broker = broker
        
        # TODO: GPIO-Pin für die LED initialisieren
        # TODO: LED-Blinken während eine Messung läuft

    def close(self):
        """
        Aufräumarbeiten bei Programmende.
        """
        # TODO: GPIO-Pin zurücksetzen
