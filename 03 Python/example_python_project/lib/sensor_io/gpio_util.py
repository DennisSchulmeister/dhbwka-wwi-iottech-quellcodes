
import sys

if sys.platform == 'armv7l':
    import RPi.GPIO as GPIO
else:
    GPIO = None

def cleanup():
    GPIO.cleanup()

def setup_temperature_sensor_resistance():
    # Der One-Wire EingangsPin wird deklariert und der integrierte
    # PullUp-Widerstand aktiviert GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Nach Aktivierung des Pull-UP Widerstandes wird gewartet,
    # bis die Kommunikation mit dem DS18B20 Sensor aufgebaut ist