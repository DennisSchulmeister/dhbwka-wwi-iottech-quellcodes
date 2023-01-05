import pygame, pygame_gui, threading

class MainWindow:
    """
    Klasse für ein einfaches User Interface auf Basis von PyGame. Zeigt, wie das
    relativ simple Event-Modell der Anwendung auch dazu genutzt werden kann, die
    Messwerte auf dem Bidlschirm darzustellen.
    
    Reagiert auf folgende Ereignisse:
    
      * distance_sensor_active(active=True/False)
      * distance_sensor_value(value=0)

    Löst folgende Ereignisse aus:
    
      * command(name="trigger-measurement")
    """
    
    def __init__(self, event_broker):
        """
        Konstruktor.
        
        @param event_broker: Zentraler Event Broker der Anwendung
        """
        self._event_broker = event_broker
        self._event_broker.add_event_listener("quit", self._on_quit)
        self._event_broker.add_event_listener("distance_sensor_active", self._on_distance_sensor_active)
        self._event_broker.add_event_listener("distance_sensor_value", self._on_distance_sensor_value)
        
        self._distance_sensor_active = False
        self._distance_sensor_value = 0
        
        self._distance_label = None
        self._quit_button = None
        self._toggle_button = None
        
        self._ui_thread = threading.Thread(target=self._ui_thread_main)
        self._ui_thread.start()

    def _on_quit(self):
        """
        Aufräumarbeiten bei Programmende.
        """
        if pygame.get_init():
            event = pygame.event.Event(pygame.QUIT)
            pygame.event.post(event)

    def _on_distance_sensor_active(self, active):
        """
        Event Listener für distance_sensor_active.
        """
        self._distance_sensor_active = active
        self._update_ui()

    def _on_distance_sensor_value(self, value):
        """
        Event Listener für distance_sensor_value.
        """
        self._distance_sensor_value = value
        self._update_ui()
    
    def _update_ui(self):
        """
        Angezeigte Werte in der Benutzeroberfläche aktualisieren
        """
        if not self._distance_sensor_active:
            self._distance_label.set_text("--- Inaktiv ---")
            self._toggle_button.set_text("Messung starten")
        else:
            distance_m = self._distance_sensor_value / 100.0
            self._distance_label.set_text("%s Meter" % distance_m)
            self._toggle_button.set_text("Messung stoppen")

    def _ui_thread_main(self):
        """
        Hauptmethode des UI-Threads. Initialisiert die Benutzeroberfläche und führt die
        Event Loop (Schleife zur Ereignisverarbeitung) des UIs aus.
        """
        pygame.init()

        pygame.display.set_caption("Einparkhilfe")
        window_surface = pygame.display.set_mode((800, 600))

        background = pygame.Surface((800, 600))
        background.fill(pygame.Color("#000000"))

        manager = pygame_gui.UIManager((800, 600))
        
        distance_label_layout_rect = pygame.Rect(10, 10, 780, 520)
        self._distance_label = pygame_gui.elements.UILabel(
            relative_rect = distance_label_layout_rect,
            anchors       = {"left": "left", "right": "right", "top": "top", "bottom": "bottom"},
            text          = "--- Inaktiv ---",
            manager       = manager
        )

        quit_button_layout_rect = pygame.Rect(0, 0, 300, 50)
        quit_button_layout_rect.bottomright = (-10, -10)
        self._quit_button = pygame_gui.elements.UIButton(
            relative_rect = quit_button_layout_rect,
            anchors       = {"left": "right", "right": "right", "top": "bottom", "bottom": "bottom"},
            text          = "Programm beenden",
            manager       = manager
        )
        
        toggle_button_layout_rect = pygame.Rect(0, 0, 300, 50)
        toggle_button_layout_rect.bottomleft = (10, -10)
        self._toggle_button = pygame_gui.elements.UIButton(
            relative_rect = toggle_button_layout_rect,
            anchors       = {"left": "left", "right": "left", "top": "bottom", "bottom": "bottom"},
            text          = "Messung starten",
            manager       = manager
        )

        clock = pygame.time.Clock()
        running = True

        while running:
            time_delta = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self._quit_button:
                            # Button: Programm beenden
                            running = False
                        elif event.ui_element == self._toggle_button:
                            # Button: Messung starten
                            self._event_broker.raise_event("command", name="trigger-measurement")

                manager.process_events(event)

            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()
        
        self._event_broker.raise_event("quit")
        self._event_broker.close()
        
        pygame.quit()
        
