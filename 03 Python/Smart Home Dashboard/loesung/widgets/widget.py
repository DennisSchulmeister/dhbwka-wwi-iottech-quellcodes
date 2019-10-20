import pygame
from pygame.locals import *
from abc import ABC, abstractmethod

class Widget(ABC):
    """
    Abstrakte Basisklasse für ein Element (Widget) auf dem Bildschirm.
    Ein Element hat eine eigene Darstellung und reagiert auf die für
    es relevanten Ereignisse wie z.B. Klick mit der Maus und so weiter.
    """
    
    def __init__(self, x, y, w, h):
        """
        Konstruktor. Nimmt die Position und Größe des Elements entgegen.
        
        @param x: X-Position
        @param y: Y-Position
        @param w: Breite
        @param h: Höhe
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @abstractmethod
    def update(self, events, surface):
        """
        Diese Methode muss vom Hauptprogramm regelmäßig aufgerufen werden,
        damit das Element die für es relevanten Ereignisse prüfen und darauf
        reagieren kann. Bei Bedarf sorgt das Element dann auch dafür, sich
        auf dem Bildschirm darzustellen.
        
        @param events:  Liste mit pygame.Event-Objekten
        @param surface: pygame.Surface des Hauptfensters
        """
        pass

    @abstractmethod
    def draw(self, surface):
        """
        Diese Methode muss von den Unterklassen ausprogrammiert werden, um
        das Element in seinem aktuellen Zustand auf den Bildschirm zu malen.
        Sie muss dementsprechend in der update-Methode aufgerufen werden,
        wenn sich sein Zustand auf darstellungsrelevante Weise ändert.
        
        Im Hauptprogramm muss diese Methode nur aufgerufen werden, wenn der
        komplette Bildschirm neugezeichnet werden soll, ohne dass dem ein
        bestimmtes Ereignis voraus geht.
        
        @param surface: pygame.Surface des Hauptfensters
        """
        pass

    def clip(self, surface, clip):
        """
        Diese Methode kann von den Unterklassen in draw() aufgerufen zu werden,
        um sicherzustellen, dass nicht über die Grenzen des Widgets hinaus auf
        den Bildschirm gemalt wird.
        
        @param surface: pygame.Surface des Hauptfensters
        @param clip: Boolean, ob die Begrenzung aktiv sein soll oder nicht
        """
        if clip:
            surface.set_clip(pygame.Rect(self.x, self.y, self.w, self.h))
        else:
            surface.set_clip(None)