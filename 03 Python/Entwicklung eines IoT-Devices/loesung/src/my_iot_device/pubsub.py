import os, threading

class PublishSubscribeBroker:
    """
    Diese Klasse implementiert einen einfachen lokalen Message Broker
    zur Umsetzung des Publish/Subscribe (oder auch Observer) Patterns.
    
    Beliebige Threads können üb er die publish()-Methode beliebige
    Nachrichten an beliebige Topics senden, wobei ein Topic hierbei
    einfach durch seinen Namen identifiziert wird und eine Nachricht
    aus den Positionsparametern (*args) und Namensparametern (**kwargs)
    der publish()-Methode besteht.
    
    Empfänger kann jede Methode sein, welche die *args und **kwargs
    der gesendeten Nachrichten verarbeiten kann. Hierfür können mit
    die Empfängermethoden mit subscribe() und unsubscribe() den Topics
    zugeordnet werden. Die Empfängermethoden werden dabei stets in
    einem eigenen Thread ausgeführt, um sie somit von den Senderthreads
    zu entkoppeln.
    """
    
    def __init__(self, threads=os.cpu_count()):
        """
        Konstruktor,
        
        @param threads: Größe des Threadpools (Default = os.cpu_count())
        """
        self._topics = {}
    
    def subscribe(self, topic, subscriber):
        """
        Hinzufügen einer Empfängermethode zu einem Topic.
        
        @param topic: Name des Topics
        @param subscriber: Empfänger-Methode
        """
        if not topic in self._topics:
            self._topics[topic] = []
        
        self._topics[topic].append(subscriber)

    def unsubscribe(self, topic, subscriber):
        """
        Entfernen einer Empfängermethode von einem Topic.
        
        @param topic: Name des Topics
        @param subscriber: Empfänger-Methode
        """
        if topic in self._topics:
            self._topics[topic].remove(subscriber)
    
    def publish(self, topic, *args, **kwargs):
        """
        Senden einer Nachricht.
        
        @param topic: Name des Topics
        @param *args: Beliebige Positionsparameter gemäß Python-Konventionen
        @param **kwargs: Beliebige Namensparameter gemäß Python-Konventionen
        """
        if not topic in self._topics:
            return
        
        for subscriber in self._topics[topic]:
            thread = threading.Thread(target=subscriber, args=args, kwargs=kwargs)
            thread.start()