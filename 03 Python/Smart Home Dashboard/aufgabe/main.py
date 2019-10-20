#! /usr/bin/env python3

# Grafisches Dashboard zur Anzeige von Temparatur- und Luftfeuchtigkeit.
# Die Werte werden über einen angeschlossenen DHT11-Sensor ermittelt und
# in Echtzeit dargestellt.
#
# Zusätzlich können anhand zweier Grenzwerte zwei LEDs zum Blinken gebracht
# werden, wenn die gemessene Temparatur zu kalt (LED1) oder zu warm (LED2) ist.
#
# Ein weiterer Button erlaubt es, ein Relais für die Zimmerbeleuchtung
# ein- oder auszuschalten.
#
# Falls das Fenster oder der Mauszeiger bei der Ausführung des Programms flimmern,
# müssen Sie noch den OpenGL-Grafiktreiber des Rasbperry Pi aktivieren. Öffnen Sie
# hierzu eine Konsole und geben Sie folgenden Befehl ein (ohne das Dollarzeichen):
#
#   $ sudo raspi-config
#
# Dort wählen Sie dann folgende Menüpunkte aus und starten den Raspberry Pi
# anschließend neu:
#
#   » Advanced Options → GL Driver → GL (Full KMS)
#   » Advanced Options → Compositor → Yes

import os, pygame

from hwio.dht11 import DHT11MockSensor
from hwio.switch import SwitchOutputDevice

from widgets.button import ButtonWidget
from widgets.graph import GraphWidget, GraphSeries
from widgets.grid import GridWidget
from widgets.label import LabelWidget
from widgets.rectangle import RectangleWidget
from widgets.window import MainWindow

def get_asset_path(filename):
    """
    Gibt den Verzeichnispfad einer Datei zurück, relativ zum Verzeichnis,
    in dem diese Quellcodedatei liegt. Ist dafür gedacht, die Pfade von
    Hintergrundbildern usw. zu ermitteln.

    @param filename: Gesuchte Datei
    @returns: Vollständiger Pfad der Datei
    """
    return os.path.join(os.path.dirname(__file__), filename)

class Main:
    """
    Dies ist die Hauptklasse des Programms. Hier werden die benötigten Objekte
    für den I/O-Zugriff auf die Hardwarebausteine erzeugt, sowie das User Interace
    aufgebaut. Wann immer eines der beteiligten Objekte eine Mitteilung für uns hat
    (Button wurde gedrückt, neuer Messwert liegt vor, …) wird eine Callback-Methode
    dieser Klasse aufgerufen, um die entsprechenden Aktionen auszulösen.
    """

    def __init__(self):
        """
        Konstruktor.
        """
        # Objekte für den Hardwarezugriff
        self.led_too_cold = SwitchOutputDevice(14)
        self.led_too_hot = SwitchOutputDevice(15)
        self.light_switch = SwitchOutputDevice(18)

        self.dht11_sensor = DHT11MockSensor(
            interval_sec = 2,
            read_cb      = self.dht11_read_cb,
        )

        self.hardware_devices = [
            self.led_too_cold,
            self.led_too_hot,
            self.light_switch,
            self.dht11_sensor,
        ]

        self.measure_on = True
        self.measure_on_label = lambda: "Messung unterbrechen" if self.measure_on else "Messung fortsetzen"

        self.light_on = False
        self.light_on_label = lambda: "Licht ausschalten" if self.light_on else "Licht einschalten"

        self.temperature_range = [9999, -9999]    # Min, Max
        self.humidity_range = [9999, -9999]       # Min, Max

        self.temperature_too_low = 22
        self.temperature_too_high = 25

        # Protokollierung der Messwerte
        csv_filename = os.path.join(os.path.expanduser("~"), "iot-dashboard.csv")
        # TODO: Klasse zur CSV-Protokollierung intialisieren

        # In open_main_window() erzeugte UI-Elemente
        # Der Überischt halber hier aufgezählt
        self.graph_widget = None
        self.label_temp_min_widget = None
        self.label_temp_max_widget = None
        self.label_humi_min_widget = None
        self.label_humi_max_widget = None
        self.button_measure_on_off = None
        self.button_clear_graph = None
        self.button_light_on_off = None

    def open_main_window(self):
        """
        Diese Methode initialisiert die Benutzeroberfläche, öffnet das Hauptfenster
        und startet die Hauptschleife des Programms. Sie wird erst beendet, nachdem
        das Fenster wieder geschlossen wurde.
        """
        pygame.font.init()

        font_heading = pygame.font.SysFont("Noto Sans Display", 26, bold=True)
        font_label = pygame.font.SysFont("Noto Sans Display", 14, bold=True)
        font_value = pygame.font.SysFont("Noto Sans Display", 14)
        font_graph = pygame.font.SysFont("Noto Sans Display", 12)

        color_heading = pygame.Color(240, 240, 240)
        color_label = pygame.Color(150, 150, 150)
        color_value = pygame.Color(240, 80, 80)

        color_graph_bg = pygame.Color(255, 255, 255, 190)
        color_graph_border = pygame.Color(255, 255, 255)
        color_graph_text = pygame.Color(30, 30, 30)
        color_graph_temperature = pygame.Color(200, 10, 10)
        color_graph_humidity = pygame.Color(10, 135, 200)

        color_button_normal = pygame.Color(75, 180, 235)
        color_button_hover = pygame.Color(75, 200, 235)
        color_button_click = pygame.Color(125, 220, 245)
        color_button_label = pygame.Color(240, 240, 240)
        color_button_border = pygame.Color(55, 135, 175)

        window_w = 1100
        window_h = 600

        self.graph_widget = GraphWidget(
            x=10, y=60, w=790, h=530,
            min_y=0, max_y=40, step_y=5, delta_x=20,
            axis_xl=5, axis_yb=20, legend_xr=5, legend_yb=20,
            font         = font_graph,
            bg_color     = color_graph_bg,
            border_color = color_graph_border,
            text_color   = color_graph_text,
            series       = [
                GraphSeries(
                    name  = "temperature",
                    label = "Temperatur in °C",
                    color = color_graph_temperature,
                    width = 3,
                ),
                GraphSeries(
                    name  = "humidity",
                    label = "Luftfeuchtigkeit in %",
                    color = color_graph_humidity,
                    width = 3,
                ),
            ],
        )

        self.label_temp_widget = LabelWidget(
            x=990, y=60, w=100, h=20,
            font=font_label, color=color_value,
            label="---",
        )

        self.label_temp_min_widget = LabelWidget(
            x=990, y=90, w=100, h=20,
            font=font_label, color=color_value,
            label="---",
        )

        self.label_temp_max_widget = LabelWidget(
            x=990, y=120, w=100, h=20,
            font=font_label, color=color_value,
            label="---",
        )

        self.label_humi_widget = LabelWidget(
            x=990, y=180, w=100, h=20,
            font=font_label, color=color_value,
            label="---",
        )

        self.label_humi_min_widget = LabelWidget(
            x=990, y=210, w=100, h=20,
            font=font_label, color=color_value,
            label="---",
        )

        self.label_humi_max_widget = LabelWidget(
            x=990, y=240, w=100, h=20,
            font=font_label, color=color_value,
            label="---",
        )

        self.label_temp_too_low = LabelWidget(
            x=990, y=300, w=100, h=20,
            font=font_label, color=color_value,
            label="---",
        )

        self.label_temp_too_high = LabelWidget(
            x=990, y=330, w=100, h=20,
            font=font_label, color=color_value,
            label="---",
        )

        self.label_temp_status = LabelWidget(
            x=820, y=360, w=270, h=20,
            font=font_label, color=color_value,
            label="",
        )

        self.button_measure_on_off = ButtonWidget(
            x=820, y=420, w=270, h=50,
            font         = font_value,
            normal_color = color_button_normal,
            hover_color  = color_button_hover,
            click_color  = color_button_click,
            label_color  = color_button_label,
            border_color = color_button_border,
            label        = self.measure_on_label(),
            click_cb     = self.button_measure_on_off_click_cb,
        )

        self.button_clear_graph = ButtonWidget(
            x=820, y=480, w=270, h=50,
            font         = font_value,
            normal_color = color_button_normal,
            hover_color  = color_button_hover,
            click_color  = color_button_click,
            label_color  = color_button_label,
            border_color = color_button_border,
            label        = "Schaubild zurücksetzen",
            click_cb     = self.button_clear_graph_click_cb,
        )

        self.button_light_on_off = ButtonWidget(
            x=820, y=540, w=270, h=50,
            font         = font_value,
            normal_color = color_button_normal,
            hover_color  = color_button_hover,
            click_color  = color_button_click,
            label_color  = color_button_label,
            border_color = color_button_border,
            label        = self.light_on_label(),
            click_cb     = self.button_light_on_off_click_cb,
        )

        widgets = [
            # Hintergrundbild: https://pixabay.com/photos/device-the-raspberry-pi-pc-3438525/
            RectangleWidget(
                x=0, y=0, w=window_w, h=window_h,
                bg_image = get_asset_path("background.jpg"),
            ),

            ## Gitter zur einfacheren Anordnung der Elemente
            #GridWidget(
            #    x=0, y=0, w=window_w, h=window_h,
            #    delta_x=10, delta_y=10, main_x=5, main_y=5,
            #    color1=pygame.Color(240,240,240,10), color2=pygame.Color(220,220,220,10),
            #),

            # Hauptüberschrift
            LabelWidget(
                x=10, y=10, w=780, h=40,
                font=font_heading, color=color_heading, #outline=True,
                label="Smart Home Dashboard – Wohnbereich",
            ),

            # Schaubild
            self.graph_widget,

            # Bezeichner der Min/Max-Werte
            LabelWidget(
                x=820, y=60, w=160, h=20,
                font=font_label, color=color_label,
                label="Temperatur:",
            ),
            LabelWidget(
                x=820, y=90, w=160, h=20,
                font=font_label, color=color_label,
                label="Temperatur Min:",
            ),
            LabelWidget(
                x=820, y=120, w=160, h=20,
                font=font_label, color=color_label,
                label="Temperatur Max:",
            ),

            LabelWidget(
                x=820, y=180, w=160, h=20,
                font=font_label, color=color_label,
                label="Luftfeuchtigkeit:",
            ),
            LabelWidget(
                x=820, y=210, w=160, h=20,
                font=font_label, color=color_label,
                label="Luftfeuchtigkeit Min:",
            ),
            LabelWidget(
                x=820, y=240, w=160, h=20,
                font=font_label, color=color_label,
                label="Luftfeuchtigkeit Max:",
            ),

            LabelWidget(
                x=820, y=300, w=160, h=20,
                font=font_label, color=color_label,
                label="Untere Temp.Grenze:",
            ),
            LabelWidget(
                x=820, y=330, w=160, h=20,
                font=font_label, color=color_label,
                label="Obere Temp.Grenze:",
            ),

            # Gemessene Min/Max-Werte
            self.label_temp_widget,
            self.label_temp_min_widget,
            self.label_temp_max_widget,

            self.label_humi_widget,
            self.label_humi_min_widget,
            self.label_humi_max_widget,

            self.label_temp_too_low,
            self.label_temp_too_high,
            self.label_temp_status,

            # Buttons
            self.button_measure_on_off,
            self.button_clear_graph,
            self.button_light_on_off,
        ]

        self.main_window = MainWindow(
            title     = "Smart Home Dashboard",
            w         = window_w,
            h         = window_h,
            fps       = 5,
            widgets   = widgets,
            update_cb = self.update_window_cb,
        )

        self.main_window.show()

    def update_window_cb(self, window, events):
        """
        Diese Methode wird in der Hauptschleife des Programms (in der Methode
        self.main_window.show()) regelmäßig aufgerufen, um Hintergrundaktivitäten
        fortzuführen und Änderngen am UI vorzunehmen.

        @param window: MainWindow-Objekt
        @param events: Liste mit pygame.Event-Objekten
        """
        for device in self.hardware_devices:
            device.tick()

    def button_measure_on_off_click_cb(self, button, data):
        """
        Button "Messung unterbrechen/fortsetzen" wurde gedrückt. Hier wird entsprechendw
        die Messung weiterer Werte unterbunden oder reaktiviert.
        """
        self.measure_on = not self.measure_on
        self.button_measure_on_off.set_label(self.measure_on_label())

    def button_clear_graph_click_cb(self, button, data):
        """
        Button "Schaubild zurücksetzen" wurde gedrückt. Hier werden alle Werte
        aus dem Schaubild entfernt, damit es wieder komplett leer ist.
        """
        # Min/Max-Werte zurücksetzen
        self.temperature_range = [9999, -9999]
        self.humidity_range = [9999, -9999]

        self.label_temp_widget.set_label("---")
        self.label_temp_min_widget.set_label("---")
        self.label_temp_max_widget.set_label("---")

        self.label_humi_widget.set_label("---")
        self.label_humi_min_widget.set_label("---")
        self.label_humi_max_widget.set_label("---")

        self.label_temp_too_low.set_label("---")
        self.label_temp_too_high.set_label("---")
        self.label_temp_status.set_label("")

        # Status-LEDs stoppen
        self.led_too_cold.switch_on(False)
        self.led_too_hot.switch_on(False)

        # Schaubild zurücksetzen
        self.graph_widget.reset()

    def button_light_on_off_click_cb(self, button, data):
        """
        Button "Licht einschalten/ausschalten" wurde gedrückt. Hier wird entsprechend
        der GPIO-Ausgang mit High oder Low belegt.
        """
        self.light_on = not self.light_on
        self.button_light_on_off.set_label(self.light_on_label())

        self.light_switch.switch_on(self.light_on)

    def dht11_read_cb(self, temperature, humidity):
        """
        Rückrufmethode für neu eingelesene DHT11-Sensordaten. Je nachdem, ob die
        Messung durchgeführt werden soll oider nicht, werden die empfangenen Werte
        hier in das Schaulbild eingetragen und in einer Messdatei protokolliert.
        """
        # Nur weiter, wenn die Messung nicht unterbrochen wurde
        if not self.measure_on:
            return

        # Min/Max-Werte durchaktualisieren
        self.temperature_range[0] = min(self.temperature_range[0], temperature)
        self.temperature_range[1] = max(self.temperature_range[1], temperature)
        self.humidity_range[0] = min(self.humidity_range[0], humidity)
        self.humidity_range[1] = max(self.humidity_range[1], humidity)

        self.label_temp_widget.set_label("%s °C" % temperature)
        self.label_temp_min_widget.set_label("%s °C" % self.temperature_range[0])
        self.label_temp_max_widget.set_label("%s °C" % self.temperature_range[1])

        self.label_humi_widget.set_label("%s %%" % humidity)
        self.label_humi_min_widget.set_label("%s %%" % self.humidity_range[0])
        self.label_humi_max_widget.set_label("%s %%" % self.humidity_range[1])

        self.label_temp_too_low.set_label("%s °C" % self.temperature_too_low)
        self.label_temp_too_high.set_label("%s °C" % self.temperature_too_high)

        if temperature < self.temperature_too_low:
            temp_status = "Es ist zu kalt!"
        elif temperature > self.temperature_too_high:
            temp_status = "Es ist zu warm!"
        else:
            temp_status = "Temperatur ist okay …"

        self.label_temp_status.set_label(temp_status)

        # Schaubild aktualisieren
        self.graph_widget.add_values({
            "temperature": temperature,
            "humidity": humidity,
        })

if __name__ == "__main__":
    Main().open_main_window()
