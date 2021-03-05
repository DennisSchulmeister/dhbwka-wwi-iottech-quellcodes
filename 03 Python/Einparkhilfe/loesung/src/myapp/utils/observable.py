import queue, threading

class Observable:
    """
    Basisklasse für Objekte, die mit dem Observer-Pattern überwacht werden könnnen.
    Kann entweder von einer Klasse geerbt werden, damit diese das Observer-Pattern
    realisiert oder als eigenständiges Objekt verwendet werden, um einen zentralen
    Event-Broker zu erhalten.
    """
    
    def __init__(self, use_event_thread=False):
        """
        Konstruktor.
        
        @param: use_event_thread: Separaten Thread verwenden, in dem die Callbacks
            ausgeführt werden, statt sie im selben Thread auszuführen, das ein
            Ereignis auslöst.
        """
        self._event_listeners = {}
        self._event_queue = None
        self._event_thread = None
        
        if use_event_thread:
            self._event_queue = queue.SimpleQueue()
            
            self._event_thread = threading.Thread(target=self._event_thread_main)
            self._event_thread.start()
    
    def add_event_listener(self, event, callback):
        """
        Registrieren einer weiteren Callback-Funktion für ein Ereignis. Diese wird
        zusammen mit den anderen Callback-Funktionen aufgerufen, sobald das überwachte
        Objekt das Ereignis auslöst.
        
        Folgende Signatur muss die Callbackfunktion haben:
        
            funktion(event, *args, **kwargs)
        
        @param event: Name des Ereignisses
        @param callback: Callback-Funktion
        """
        if not event in self._event_listeners:
            self._event_listeners[event] = []
        
        self._event_listeners[event].append(callback)
    
    def remove_event_listener(self, event, callback):
        """
        Deregistrierung einer Callback-Funktion.
        
        @param event: Name des Ereignisses
        @param callback: Callback-Funktion
        """
        if event in self._event_listeners and callback in self._event_listeners[event]:
            self._event_listeners[event].remove(callback)
    
    def raise_event(self, event, *args, **kwargs):
        """
        Methode zum Auslösen eines Ereignisses. Als erster Parameter muss der Name des
        Ereignisses übergeben werden. Danach können beliebige weitere Parameter folgen,
        die unverändert an die Callback-Funktionen weitergegeben werden.
        
        Es gilt zu beachten, dass die Callback-Funktionen im selben Thread laufen,
        der das Ereignis auslöst.
        
        @param event: Name des Ereignisses
        @param *args: Beliebige Positionsparameter gemäß Python-Konventionen
        @param **kwargs: Beliebige Namensparameter gemäß Python-Konventionen
        """
        if not event in self._event_listeners:
            return
        
        if self._event_queue:
            # Event in die Warteschlange für den Event Thread stellen
            self._event_queue.put({
                "type": "event",
                "event": event,
                "args": args,
                "kwargs": kwargs,
            })
        else:
            # Callbacks im rufenden Thread direkt ausführen
            for callback in self._event_listeners[event]:
                callback(*args, **kwargs)
    
    def close(self):
        """
        Event Thread beenden, sobald alle anstehenden Ereignisse abgearbeitet wurden.
        Bewirkt nichts, wenn dem Konstruktor `use_event_thread = False` mitgegeben wurde.
        """
        if self._event_queue:
            self._event_queue.put({"type": "close"})
    
    def join_thread(self):
        """
        Den Aufrufer so lange blockieren, wie der Event Thread läuft.
        """
        if self._event_thread:
            self._event_thread.join()

    def _event_thread_main(self):
        """
        Hauptmethode des Event Threads, in dem die Callbacks ausgeführt werden, wenn dem
        Konstruktor der Parameter `use_event_thread = True` mitgegeben wurde.
        """
        running = True
        
        while running:
            command = self._event_queue.get()
            
            if command["type"] == "event":
                # Callbacks zu einem Event ausführen
                for callback in self._event_listeners[command["event"]]:
                    callback(*command["args"], **command["kwargs"])
            elif command["type"] == "close":
                # Event Thread beenden und keine weiteren Events mehr bearbeiten
                running = False
        
