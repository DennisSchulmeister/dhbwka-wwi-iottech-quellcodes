import logging

class ConsoleLogHandler:
    """
    Subscriber-Klasse, die verschiedene Nachrichten vom Messagebroker empfängt
    und auf der Konsole ausgibt. Somit sehen wir auf der Konsole immer, was
    gerade passiert.
    """
    
    def __init__(self, broker):
        """
        Konstruktor.
        
        @param broker: Zentraler PublishSubscribeBroker der Anwendung
        """
        self._broker = broker
        self._broker.subscribe("air-sensor/command", self._air_sensor_command_cb)
        self._broker.subscribe("air-sensor/status", self._air_sensor_status_cb)
        self._broker.subscribe("air-sensor/values", self._air_sensor_values_cb)
        self._broker.subscribe("database/status", self._database_status_cb)
        
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.INFO)
    
        formatter = logging.Formatter("[%(asctime)s] %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

    def _air_sensor_command_cb(self, command):
        """
        Subscriber für das Topic "air-sensor/command".
        """
        self._logger.info("air-sensor/command: %s" % command)

    def _air_sensor_status_cb(self, status):
        """
        Subscriber für das Topic "air-sensor/status".
        """
        self._logger.info("air-sensor/status: %s" % status)

    def _air_sensor_values_cb(self, **kwargs):
        """
        Subscriber für das Topic "air-sensor/values".
        """
        self._logger.info("air-sensor/values: t = %(t)s °C, h = %(h)s %%" % kwargs)
    
    def _database_status_cb(self, status):
        """
        Subscriber für das Topic "database/status".
        """
        self._logger.info("database/status: %s" % status)