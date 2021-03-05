import RPi.GPIO as GPIO
import queue, threading, time

class DistanceSensor:
    """
    Handler-Klasse für den Ultraschallsensor.
    
    Regaiert auf folgende Ereignisse:
    
      * command(name="trigger-measurement")
      
    Löst folgende Ereignisse aus:
    
      * distance_sensor_active(active=True/False)
      * distance_sensor_value(value=0)
    """
    
    def __init__(self, event_broker, gpio_pin_trigger, gpio_pin_echo):
        """
        Konstruktor.
        
        @param event_broker: Zentraler Event Broker der Anwendung
        @param gpio_pin_trigger: GPIO-Nummer des Trigger-Ausgangs
        @param gpio_pin_echo: GPIO-Nummer des Echo-Eingangs
        """
        self._event_broker = event_broker
        self._gpio_pin_trigger = gpio_pin_trigger
        self._gpio_pin_echo = gpio_pin_echo
        self._distance_sensor_active = False
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin_trigger, GPIO.OUT)
        GPIO.setup(gpio_pin_echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.output(gpio_pin_trigger, False)
        
        self._command_queue = queue.SimpleQueue()
        self._command_thread = threading.Thread(target=self._command_thread_main)
        self._command_thread.start()

        event_broker.add_event_listener("quit", self._on_quit)
        event_broker.add_event_listener("command", self._on_command)
        
    def _on_quit(self):
        """
        Aufräumarbeiten bei Programmende.
        """
        self._command_queue.put("close")
        self._command_thread.join()
        
        GPIO.cleanup(self._gpio_pin_trigger)
        GPIO.cleanup(self._gpio_pin_echo)
    
    def _on_command(self, name):
        """
        Callback für das command-Ereignis, um die Messung zu starten oder
        zu stoppen. Der empfangene Befehl wird hier in eine blockierende
        Queue gestellt, um vom Command Thread abgearbeitet zu werden.
        """
        self._command_queue.put(name)
    
    def _command_thread_main(self):
        """
        Hauptmethode des Command Threads, in dem die empfangenen Befehle abgearbeitet
        und die Messungen vorgenommen werden. Ein eigener Thread kommt hier zum Einsatz,
        weil für die Messung der aktuelle Thread mehrfach unterbrochen werden muss,
        dadurch aber nicht das gesamte Programm hängen soll.
        """
        running = True
        
        while running:
            # Empfangene Kommandos abarbeiten
            try:
                command = self._command_queue.get(timeout=0.25)
            except queue.Empty:
                command = ""
            
            if command == "trigger-measurement":
                # Messung starten oder stoppen
                self._distance_sensor_active = not self._distance_sensor_active
                self._event_broker.raise_event("distance_sensor_active", active=self._distance_sensor_active)
            elif command == "close":
                # Thread beenden
                running = False
            
            # Messung vornehmen, falls der Sensor aktiv ist
            if self._distance_sensor_active:
                # Messung durch einen 10µS Impuls am Trigger-Ausgang starten
                GPIO.output(self._gpio_pin_trigger, True)
                time.sleep(0.00001)
                GPIO.output(self._gpio_pin_trigger, False)
                
                # Dauer des Impuls am Echo-Eingang messen, um die Entfernung zu ermitteln
                # Die Entfernung ergibt sich dann aus dem mittleren Schalleschwindigkeit von 343,2 m/S
                # geteilt durch 2, weil der Schall die doppelte Strecke zurücklegt (hin zum Hinderniss
                # und zurück).
                measure_start_time = time.time()
                echo_start_time = measure_start_time
                echo_stop_time = measure_start_time
                
                while not GPIO.input(self._gpio_pin_echo):
                    echo_start_time = time.time()
                    
                    if (echo_start_time - measure_start_time) > 1.5:
                        break
                
                while GPIO.input(self._gpio_pin_echo):
                    echo_stop_time = time.time()
                    
                    if (echo_stop_time - measure_start_time) > 1.5:
                        break
                
                distance_cm = round(((echo_stop_time - echo_start_time) * 34320) / 2)
                
                if distance_cm >= 2 and distance_cm <= 300:
                    self._event_broker.raise_event("distance_sensor_value", value=distance_cm)
        