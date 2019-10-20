from abc import ABC, abstractmethod

class HardwareDevice(ABC):
    """
    Abstrakte Basisklasse für einen mit der Anwender angesprochendes Hardwarebaustein.
    Diese Klasse definiert lediglich die tick()-Methode, die in der Hauptschleife des
    Programms regelmäßig aufgerufen werden muss, um den Status des Bausteins zu aktualisieren,
    sowie die close()-Methode zum Beenden des Hardwarezugriffs.
    """
    
    @abstractmethod
    def tick(self):
        """
        Diese Methode muss in der Hauptschleife des Programms regelmäßig aufgerufen
        werden. Die erbenden Klassen können diese dann überschreiben, um zeitabhängige
        Aktionen (wie das Blinken einer LED) vorzunehmen.
        
        WICHTIG: Die überschriebene Methode darf nicht blockieren. Soll zum Beispiel
        eine LED zum Blinken gebracht werden, darf hier nicht einfach mit sleep()
        der rufende Thread unterbrochen werden. Stattdessen muss geprüft werden, ob
        genügend Zeit vergangen ist, bevor die LED ein oder wieder ausgeschaltet wird.
        In jedem Fall ist die Methode so schnell wie möglich wieder zu verlassen.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Diese Methode muss im Hauptprogramm aufgerufen werden, wenn das Hardwarelement
        nicht mehr benötigt wird.
        """
        pass