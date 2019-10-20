import pygame
from pygame.locals import *
from .widget import Widget

class GridWidget(Widget):
    """
    Hilfsklasse zum Zeichnen eines Gitters, anhand dessen die Pixelpositionen
    Elemente dann leichter abgelesen werden können.
    """
    
    def __init__(self, x, y, w, h, delta_x, delta_y, main_x, main_y, color1, color2):
        """
        Konstruktor.
        
        @param x:       X-Position
        @param y:       Y-Position
        @param w:       Breite
        @param h:       Höhe
        @param delta_x: Rastergröße in X-Richtung
        @param delta_y: Rastergröße in Y-Richtung
        @param main_x:  Eine vertikale Hauptlinie alle x Kästchen
        @param main_y:  Eine horizontale Hauptlinie alle y Kästchen
        @param color1:  pygame.Color-Objekt der Gitterlinien
        @param color2:  pygame.Color-Objekt der Hauptlinien
        """
        super().__init__(x, y, w, h)
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.main_x = main_x
        self.main_y = main_y
        self.color1 = color1
        self.color2 = color2
        
        self._redraw = True
    
    def update(self, events, surface):
        """
        Für das Element relevante Ereignisse prüfen und verarbeiten.
        
        @param events:  Liste mit pygame.Event-Objekten
        @param surface: pygame.Surface des Hauptfensters
        """
        for event in events:
            pass
        
        if self._redraw:
            self.draw(surface)

    def draw(self, surface):
        """
        Element auf den Bildschirm zeichnen.
        @param surface: pygame.Surface des Hauptfensters
        """
        self.clip(surface, True)
        
        for x in range(0, self.w, self.delta_x):
            pygame.draw.line(surface, self.color1, (x, 0), (x, self.h))
        
        for y in range(0, self.h, self.delta_y):
            pygame.draw.line(surface, self.color1, (0, y), (self.w, y))

        for x in range(0, self.w, self.delta_x * self.main_x):
            pygame.draw.line(surface, self.color2, (x, 0), (x, self.h))
        
        for y in range(0, self.h, self.delta_y * self.main_y):
            pygame.draw.line(surface, self.color2, (0, y), (self.w, y))
            
        self.clip(surface, False)
        self._redraw = False
