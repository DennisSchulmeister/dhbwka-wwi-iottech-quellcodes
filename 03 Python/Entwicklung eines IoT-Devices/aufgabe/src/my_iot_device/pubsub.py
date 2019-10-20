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
    pass
    # TODO