import math, pygame
from pygame.locals import *
from .widget import Widget

class GraphSeries:
    """
    Hilfsobjekt für die GraphWidget-Klasse. Dem Konstruktor von GraphWidget
    muss eine Liste mit GraphSeries-Objekten, von denen jedes für eine im
    Schaubild darzustellende Datenreihe steht, übergeben werden.
    """
    
    def __init__(self, name, label, color, width):
        """
        Konstruktor
        
        @param name:  Technischer Name der Datenreihe
        @param label: Darzustellender Name der Datenreihe
        @param color: pygame.Color mit der Farbe der Datenreihe
        @param width: Dicke der Linie
        """
        self.name = name
        self.label = label
        self.color = color
        self.width = width

class GraphWidget(Widget):
    """
    Die Königin unter den Widgets. Diese Klasse zeichnet ein sicht stets
    aktualisierendes Liniendiagramm mit mehreren Messwerten. Zusätzlich
    können bis zu zwei Grenzwerte dargestellt und vom Anwender interaktiv
    verändert werden.
    """
    
    def __init__(self, x, y, w, h, series, min_y, max_y, step_y, delta_x,
                 axis_xl, axis_yb, legend_xr, legend_yb,
                 font, bg_color, border_color, text_color):
        """
        Konstruktor.
        
        @param x:            X-Position
        @param y:            Y-Position
        @param w:            Breite
        @param h:            Höhe
        @param min_y:        Mindestwert der Y-Skala
        @param max_y:        Maximalwert der Y-Skala
        @param step_y:       Schrittweite der Y-Skala
        @param delta_x:      X-Abstand zwischen zwei Werten
        @param axis_xl:      X-Position der Skala von links
        @param axis_yb:      Y-Position der Skala von unten
        @param legend_xr:    X-Position der Legende von rechts
        @param legend_yb:    Y-Position der Legende von unten
        @param series:       Liste von GraphSeries-Objekten
        @param font:         pygame.Font-Objekt der Schriftart
        @param bg_color:     pygame.Color-Objekt der Hintergrundfarbe
        @param border_color: pygame.Color-Objekt der Linienfarbe
        @param text_color:   pygame.Color-Objekt der Schriftfarbe
        """
        super().__init__(x, y, w, h)
        self.min_y = min_y
        self.max_y = max_y
        self.step_y = step_y
        self.delta_x = delta_x
        self.axis_xl = axis_xl
        self.axis_yb = axis_yb
        self.legend_xr = legend_xr
        self.legend_yb = legend_yb
        self.series = series
        self.font = font
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color
        
        self._data = []
        self._redraw = True
        self._bg_backup = None
    
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

    def add_values(self, values):
        """
        Fügt dem Schaubild weitere Werte hinzu.
        
        @param values: Dictionary mit den neuen Werten,
                       Key ist der technische Name der Datenreihe,
                       Value der numerische Messwert
        """
        self._data.append(values)
        self._redraw = True

    def reset(self):
        """
        Löscht alle Werte und setzt das Schaubild wieder zurück.
        """
        self._data = []
        self._redraw = True

    def draw(self, surface):
        """
        Element auf den Bildschirm zeichnen. Damit das Schaubild jederzeit geändert
        werden kann, wird hier eine Sicherungskopie des vom Schaubild überdeckten
        Hintergrunds gemacht. Bei einer Änderung wird der Hintergrund anhand dieser
        Kopie erst wiederhergestellt, bevor das neue Schaubild gemalt wird.
        
        @param surface: pygame.Surface des Hauptfensters
        """
        self.clip(surface, True)
        
        if self._bg_backup:
            surface.blit(self._bg_backup, (self.x, self.y))
        else:
            self._bg_backup = pygame.Surface((self.w, self.h))
            self._bg_backup.blit(surface, (0,0), pygame.Rect(self.x, self.y, self.w, self.h))
            
        graph_surface = pygame.Surface((self.w, self.h), SRCALPHA)
        graph_surface.fill(self.bg_color)
        
        self._draw_grid(graph_surface)
        self._draw_data(graph_surface)
        self._draw_axis(graph_surface)
        self._draw_legend(graph_surface)
        
        pygame.draw.rect(graph_surface, self.border_color, pygame.Rect(0, 0, self.w, self.h), 1)
        
        surface.blit(graph_surface, (self.x, self.y))
        self.clip(surface, False)
        self._redraw = False
    
    def _draw_grid(self, surface):
        """
        Gitternetzlinien zeichnen
        @param surface: pygame.Surface-Objekt zum Zeichnen
        """
        values = []
        
        for y in range(self.min_y, self.max_y, self.step_y):
            values.append(y)
        if not values[-1] == self.max_y:
            values.append(self.max_y)
        
        x = self.axis_xl
        y = self.h - self.axis_yb
        margin = y / (len(values) - 1)
        
        for value in values:
            pygame.draw.line(surface, self.border_color, (0, y), (self.w, y))
            y -= margin
    
    def _draw_axis(self, surface):
        """
        Axenbeschritungen zeichen
        @param surface: pygame.Surface-Objekt zum Zeichnen
        """
        values = []
        
        for y in range(self.min_y, self.max_y, self.step_y):
            values.append(y)
        if not values[-1] == self.max_y:
            values.append(self.max_y)
        
        x = self.axis_xl
        y = self.h - self.axis_yb
        margin = y / (len(values) - 1)
        
        for value in values:
            text_surface = self.font.render(str(value), True, self.text_color)
            surface.blit(text_surface, (x, y))
            y -= margin
    
    def _draw_data(self, surface):
        """
        Datenlinien zeichen
        @param surface: pygame.Surface-Objekt zum Zeichnen
        """
        amount_data = math.floor(self.w / self.delta_x)
        
        if amount_data < len(self._data):
            self._data = self._data[-amount_data:]
        
        for series in self.series:
            prev_value = 0
            y = None
            x = 0
            
            for values in self._data:
                if series.name in values:
                    value = values[series.name]
                else:
                    value = prev_value
                prev_value = value
                
                y1 = self.h - (self.h / (self.max_y - self.min_y) * (value - self.min_y))
                x1 = x + self.delta_x
                
                if y != None:
                    pygame.draw.line(surface, series.color, (x, y), (x1, y1), series.width)
                
                x = x1
                y = y1
    
    def _draw_legend(self, surface):
        """
        Legende der Datenreihen zeichen
        @param surface: pygame.Surface-Objekt zum Zeichnen
        """
        text_surfaces = []
        
        for series in self.series:
            text_surface = self.font.render(series.label, True, series.color)
            text_surfaces.append(text_surface)
        
        x = self.w - self.legend_xr
        y = self.h - self.legend_yb
        margin = 20
        
        for text_surface in text_surfaces:
            x -= text_surface.get_width()
            surface.blit(text_surface, (x, y))
            x -= margin