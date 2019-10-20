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

        # TODO: GPIO-Pin für den Button initialisieren
        # TODO: Neue Messung anstoßen, wenn der Button gedrückt wird

    def close(self):
        """
        Aufräumarbeiten bei Programmende.
        """
        # TODO: GPIO-Pin zurücksetzen