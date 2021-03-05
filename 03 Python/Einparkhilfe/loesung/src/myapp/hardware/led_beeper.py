import RPi.GPIO as GPIO
import queue, threading

class LedBeeper:
    """
    Handler-Klasse für die LED und den Piepser. Empfängt die Messwerte vom Ultraschallsensor und
    lässt die LED und den Piepser immer schneller blinken und tönen, je geringer der Abstand ist.
    
    Regaiert auf folgende Ereignisse:
    
      * distance_sensor_active(active=True/False)
      * distance_sensor_value(value=0)
      
    Löst folgende Ereignisse aus:
    
      * Keine
    """
    
    def __init__(self, event_broker, gpio_pin_led, gpio_pin_beeper,
                 distance_cm_min, distance_cm_max,
                 frequency_hz_min, frequency_hz_max):
        """
        Konstruktor.
        
        @param event_broker: Zentraler Event Broker der Anwendung
        @param gpio_pin_led: GPIO-Nummer der LED
        @param gpio_pin_beeper: GPIO-Nummer des Piepsers
        @param distance_cm_min: Dauerton bei kleineren oder gleichen Abständen in cm
        @param distance_cm_max: Kein Ton bei größeren Abstände in cm
        @param frequency_hz_min: Frequenz in Hz bei Mindestabstand
        @param frequency_hz_max: Frequenz n Hz bei Maximalabstand
        """
        self._event_broker = event_broker
        self._gpio_pin_led = gpio_pin_led
        self._gpio_pin_beeper = gpio_pin_beeper
        self._distance_cm_min = distance_cm_min
        self._distance_cm_max = distance_cm_max
        self._frequency_hz_min = frequency_hz_min
        self._frequency_hz_max = frequency_hz_max
        
        self._distance_sensor_active = False
        self._distance_sensor_value = 0
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin_led, GPIO.OUT)
        GPIO.setup(gpio_pin_beeper, GPIO.OUT)
        GPIO.output(gpio_pin_led, False)
        GPIO.output(gpio_pin_beeper, False)
        
        self._pwm_led = GPIO.PWM(gpio_pin_led, 1)
        self._pwm_beeper = GPIO.PWM(gpio_pin_beeper, 1)
     
        event_broker.add_event_listener("quit", self._on_quit)
        event_broker.add_event_listener("distance_sensor_active", self._on_distance_sensor_active)
        event_broker.add_event_listener("distance_sensor_value", self._on_distance_sensor_value)

    def _on_quit(self):
        """
        Aufräumarbeiten bei Programmende.
        """        
        GPIO.cleanup(self._gpio_pin_led)
        GPIO.cleanup(self._gpio_pin_beeper)
    
    def _on_distance_sensor_active(self, active):
        """
        Event Listener für distance_sensor_active.
        """
        self._distance_sensor_active = active
        self._sound_the_alarm()

    def _on_distance_sensor_value(self, value):
        """
        Event Listener für distance_sensor_value.
        """
        self._distance_sensor_value = value
        self._sound_the_alarm()
    
    def _sound_the_alarm(self):
        # Frequenz linear ansteigen lassen, je geringer der Abstand
        # Der Wert ergibt sich durch Auflösen der linearen Gleichung frequency = (m * distance) + c
        enable = False
        pwm = False
        frequency_hz = 0
        delta_distance_cm = 0
        
        if not self._distance_sensor_active:
            pass
        elif self._distance_sensor_value > self._distance_cm_max:
            pass
        elif self._distance_sensor_value < self._distance_cm_min:
            enable = True
        else:
            enable = True
            pwm = True
            
            delta_frequency_hz = self._frequency_hz_max - self._frequency_hz_min * 1.0
            delta_distance_cm = self._distance_cm_max - self._distance_cm_min * 1.0
            m = delta_frequency_hz / delta_distance_cm
            c = self._frequency_hz_max - (m * self._distance_cm_max)
            frequency_hz = (m * self._distance_sensor_value) + c
        
        if not enable:
            # Kein Ton und keine LED
            self._pwm_led.stop()
            GPIO.output(self._gpio_pin_led, False)
            
            self._pwm_beeper.stop()
            GPIO.output(self._gpio_pin_beeper, False)
        elif not pwm:
            # LED und Beeper dauerhaft aktiv
            self._pwm_led.stop()
            GPIO.output(self._gpio_pin_led, True)
            
            self._pwm_beeper.stop()
            GPIO.output(self._gpio_pin_beeper, True)
        else:
            # Frequenz abhängg vom Abstand
            self._pwm_beeper.ChangeFrequency(frequency_hz)
            self._pwm_beeper.start(50)
            
            self._pwm_led.ChangeFrequency(frequency_hz)
            self._pwm_led.start(50)
    