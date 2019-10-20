import pygame
from pygame.locals import *
from .widget import Widget

class RectangleWidget(Widget):
    """
    Ein farbiger Bereich, optional mit Hintergrundfarbe, Hintergrundbild
    und Rahmen.
    """
    
    def __init__(self, x, y, w, h, bg_color=None, bg_image="", border_color=None, border_width=1):
        """
        Konstruktor.
        
        @param x:            X-Position
        @param y:            Y-Position
        @param w:            Breite
        @param h:            Höhe
        @param bg_color:     pygame.Color der Hintergrundfarbe (optional)
        @param bg_image:     Dateipfad des Hintergrundbilds (optional)
        @param border_color: pygame.Color der Rahmenfarbe (optional)
        @param border_width: Dicke des Rahmens (optional)
        """
        super().__init__(x, y, w, h)
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        
        if bg_image:
            self.bg_image_surface = pygame.image.load(bg_image)
            self.bg_image_surface = pygame.transform.scale(self.bg_image_surface, (self.w, self.h))
        else:
            self.bg_image_surface = None
        
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
        
        if self.bg_color:
            surface.fill(self.bg_color)
        
        if self.bg_image_surface:
            self.bg_image_surface = self.bg_image_surface.convert()
            surface.blit(self.bg_image_surface, (self.x, self.y))
        
        if self.border_color and self.border_width:
            pygame.draw.rect(surface, self.border_color,
                             pygame.Rect(self.x, self.y, self.w, self.h),
                             self.border_width)
        
        self.clip(surface, False)
        self._redraw = False

