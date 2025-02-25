import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
gas_pin = 7  # Example GPIO pin
GPIO.setup(gas_pin, GPIO.IN)

try:
    while True:
        if GPIO.input(gas_pin):
            print("Gas detected!")
        else:
            print("No gas detected.")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()