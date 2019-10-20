from abc import ABC, abstractmethod

class DataLogger(ABC):
    """
    Abstrakte Basisklasse für Objekte, welche die Messwerte protokollieren
    oder über das Internet an einen Backendserver verschicken können.
    """
    
    @abstractmethod
    def log_values(self, temperature, humidity, light_switch):
        """
        Diese Methode muss aufgerufen werden, sobald neue Werte vorliegen,
        bzw. ein neuer Datensatz protokolliert werden soll.
        """
        pass