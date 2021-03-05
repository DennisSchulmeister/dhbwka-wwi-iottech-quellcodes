import logging

class ConsoleLogger:
    """
    Klasse, die verschiedene Nachrichten vom Messagebroker empfängt und auf der
    Konsole ausgibt. Somit sehen wir auf der Konsole immer, was gerade passiert.
    """

    def __init__(self, event_broker):
        """
        Konstruktor.
        
        @param event_broker: Zentraler Event Broker der Anwendung
        """
        self._event_broker = event_broker
        self._event_broker.add_event_listener("command", self._on_command)
        self._event_broker.add_event_listener("distance_sensor_active", self._on_distance_sensor_active)
        self._event_broker.add_event_listener("distance_sensor_value", self._on_distance_sensor_value)
        
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.INFO)
    
        formatter = logging.Formatter("[%(asctime)s] %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
    
    def _on_command(self, name):
        self._logger.info("command: %s" % name)
    
    def _on_distance_sensor_active(self, active):
        self._logger.info("distance_sensor_active: %s" % active)
    
    def _on_distance_sensor_value(self, value):
        self._logger.info("distance_sensor_value: %s" % value)