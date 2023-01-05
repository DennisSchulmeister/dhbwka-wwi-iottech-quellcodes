import time, pygame
from pygame.locals import *

class MainWindow:
    """
    Hauptklasse der Benutzeroberfläche. Diese Klasse erzeugt das Hauptfenster
    und kümmert sich darum, alle darin enthaltenen Elemente regelmäßig neu
    zu zeichnen.
    """

    def __init__(self, title, w, h, fps, widgets, update_cb=None):
        """
        Konstruktor.
        
        @param title:     Titel
        @param w:         Breite
        @param h:         Höhe
        @param fps:       Anzahl Aktualisierungen je Sekunde
        @param widgets:   Liste der darzustellenden Widgets
        @param update_cb: Periodische Rückruffunktion
        
        Die Rückruffunktion wird innerhalb der Hauptschleife des Programms
        aufgerufen, bevor alle anderen Ereignisse abgearbeitet werden. Somit
        kann an einer zentralen Stelle auf äußere Einflüße reagiert werden,
        um das UI zu aktualisieren. Die Funktion muss folgende Signatur haben:
        
        def window_update_cb(window, events):
            …
        """
        self.title = title
        self.w = w
        self.h = h
        self.fps = fps
        self.widgets = widgets
        self.update_cb = update_cb
        
        pygame.init()
        self._surface = None
        self._fps_prev_sleep = time.perf_counter()

    def show(self):
        """
        Hier wird das Hauptfenster geöffnet und die Hauptschleife des
        Programms ausgeführt. Die Methode kehrt erst zurück, wenn das
        Fenster vom Anwender geschlossen wurde.
        """
        self._surface = pygame.display.set_mode((self.w, self.h), DOUBLEBUF, 32)
        pygame.display.set_caption(self.title)
        self._surface.fill((255, 255, 255))
        
        quit = False
        while not quit:
            events = pygame.event.get()
            
            if self.update_cb:
                self.update_cb(self, events)
            
            for event in events:
                if event.type == QUIT:
                    quit = True
            
            for widget in self.widgets:
                widget.update(events, self._surface)
                
            pygame.display.flip()
            self._sleep_with_constant_fps()

        pygame.quit()

    def _sleep_with_constant_fps(self):
        """
        Diese Methode sorgt dafür, dass das Programm nicht die gesamte CPU auslastet,
        dabei aber dennoch eine konstante Framerate für den Bildaufbau erzielt. Sie
        muss hierfür in der Hauptschleife des Programms periodisch aufgerufen werden.
        Dabei misst sie dann die Zeit, die seit dem letzten Aufruf vergangen ist,
        zieht diese von der rechnerischen Wartezeit zwischen zwei Bildern ab und legt
        den rufenden Thread dann entsprechend schlafen.
        """
        now = time.perf_counter()
        delta = self.fps - now - self._fps_prev_sleep
        self._fps_prev_sleep = now
        
        if delta > 0:
            time.sleep(delta)
