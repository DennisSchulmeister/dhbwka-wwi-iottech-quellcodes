import pygame
from pygame.locals import *
from .widget import Widget

class ButtonWidget(Widget):
    """
    Ein einfacher Button, den der Anwender anklicken kann, um eine
    Aktion auszulösen.
    """
    
    STATE_NORMAL  = 0
    STATE_HOVER   = 1
    STATE_BTNDOWN = 2
    
    def __init__(self, x, y, w, h, label, font,
                 normal_color=None, hover_color=None, click_color=None,
                 label_color=None, border_color=None,
                 click_cb=None, data=None):
        """
        Konstruktor.
        
        @param x:            X-Position
        @param y:            Y-Position
        @param w:            Breite
        @param h:            Höhe
        @param label:        Beschriftung
        @param font:         pygame.Font-Objekt der Schriftart
        @param normal_color: pygame.Color-Objekt der Hintergrundfarbe (normal)
        @param hover_color:  pygame.Color-Objekt der Hintergrundfarbe (hover)
        @param click_color:  pygame.Color-Objekt der Hintergrundfarbe (click)
        @param label_color:  pygame.Color-Objekt der Textfarbe
        @param border_color: pygame.Color-Objekt der Rahmenfarbe
        @param click_cb:     Rückruffunktion bei Klick des Buttons (optional)
        @param data:         Zusatzdaten für die Rückfruffunktion (optional)
        
        Die Callback-Funktion muss folgende Signatur besitzen:
        
        def button_clicked_cb(button_widget, data):
            …
        """
        super().__init__(x, y, w, h)
        self.label = label
        self.font = font
        self.label_color = label_color
        self.border_color = border_color
        self.label_color = label_color
        self.click_cb = click_cb
        self.data = data
        
        self.bg_color = {
            self.STATE_NORMAL:  normal_color,
            self.STATE_HOVER:   hover_color,
            self.STATE_BTNDOWN: click_color,
        }
        
        self.max_x = self.x + self.w
        self.max_y = self.y + self.h

        self._state = self.STATE_NORMAL
        self._redraw = True
        
    def set_label(self, label):
        """
        Diese Methode setzt einen neuen Text für den Button.
        """
        self.label = label
        self._redraw = True
        
    def update(self, events, surface):
        """
        Für das Element relevante Ereignisse prüfen und verarbeiten.
        
        @param events:  Liste mit pygame.Event-Objekten
        @param surface: pygame.Surface des Hauptfensters
        """
        def _in_bounding_rect(event):
               return event.pos[0] >= self.x and \
                      event.pos[0] <= self.max_x and \
                      event.pos[1] >= self.y and \
                      event.pos[1] <= self.max_y

        def _set_new_state(state):
            if self._state != state:
                self._state = state
                self._redraw = True

        for event in events:
            if event.type == MOUSEMOTION and not event.buttons[0]:
                # Mausknopf nicht betätigt, ist der Cursor über dem Button?
                if _in_bounding_rect(event):
                    _set_new_state(self.STATE_HOVER)
                else:
                    _set_new_state(self.STATE_NORMAL)
            elif event.type == MOUSEBUTTONDOWN:
                # Mausknopf noch huntergedrückt, ist der Cursor über dem Button?
                if _in_bounding_rect(event):
                    _set_new_state(self.STATE_BTNDOWN)
            elif event.type == MOUSEBUTTONUP:
                # Mausknopf wieder losgelassen, ist der Cursor über dem Button?
                if _in_bounding_rect(event):
                    _set_new_state(self.STATE_HOVER)
                    
                    # Callback-Funktion hier aufrufen
                    if self.click_cb:
                        self.click_cb(self, self.data)
                else:
                    _set_new_state(self.STATE_NORMAL)

        if self._redraw:
            self.draw(surface)

    def draw(self, surface):
        """
        Element auf den Bildschirm zeichnen.
        @param surface: pygame.Surface des Hauptfensters
        """
        self.clip(surface, True)
        
        bg_color = self.bg_color[self._state]
        if bg_color:
            surface.fill(bg_color)
        
        if self.label and self.label_color:
            label_surface = self.font.render(self.label, True, self.label_color)
            center_x = (self.w - label_surface.get_width()) / 2
            center_y = (self.h - label_surface.get_height()) / 2
            surface.blit(label_surface, (self.x + center_x, self.y + center_y))
        
        if self.border_color:
            pygame.draw.rect(surface, self.border_color,
                             pygame.Rect(self.x, self.y, self.w, self.h), 1)
        
        self.clip(surface, False)
        self._redraw = False
