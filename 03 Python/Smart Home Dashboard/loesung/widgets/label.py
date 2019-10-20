import pygame
from pygame.locals import *
from .widget import Widget

class LabelWidget(Widget):
    """
    Ein einfaches Label mit einem statischen Text.
    """
    
    def __init__(self, x, y, w, h, font, color, label, outline=False):
        """
        Konstruktor.
        
        @param x:       X-Position
        @param y:       Y-Position
        @param w:       Breite
        @param h:       Höhe
        @param font:    pygame.Font-Objekt der Schriftart
        @param color:   pygame.Color-Objekt der Schriftfarbe
        @param label:   Text des Labels
        @param outline: Rahmen um das Label zeichnen
        """
        super().__init__(x, y, w, h)
        self.font = font
        self.color = color
        self.label = label
        self.outline = outline
        
        self._redraw = True
        self._bg_backup = None
    
    def set_label(self, label):
        """
        Diese Methode setzt einen neuen Anzeigetext für das Label.
        """
        self.label = label
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
        Element auf den Bildschirm zeichnen. Damit das Label jederzeit geändert
        werden kann, wird hier eine Sicherungskopie des vom Label überdeckten
        Hintergrunds gemacht. Bei einer Änderung des Textes wird der Hintergrund
        anhand dieser Kopie erst wiederhergestellt, bevor der neue Text gemalt
        wird.
        
        @param surface: pygame.Surface des Hauptfensters
        """
        self.clip(surface, True)
        
        if self._bg_backup:
            surface.blit(self._bg_backup, (self.x, self.y))
        
        text_surface = self.font.render(self.label, True, self.color)
        self._bg_backup = pygame.Surface((text_surface.get_width(), text_surface.get_height()))
        self._bg_backup.blit(surface, (0,0), pygame.Rect(self.x, self.y, text_surface.get_width(), text_surface.get_height()))
        surface.blit(text_surface, (self.x, self.y))
        
        if self.outline:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.w, self.h), 1)

        self.clip(surface, False)
        self._redraw = False
