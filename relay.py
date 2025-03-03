import RPi.GPIO as GPIO
import time

# Define GPIO pins for relays
AC_RELAY_PIN = 24  # IN1
HEAT_RELAY_PIN = 27 # IN2
FAN_HIGH_RELAY_PIN = 22 # IN3
FAN_LOW_RELAY_PIN = 23 # IN4

# Set GPIO mode
GPIO.setmode(GPIO.BCM) 

# Setup GPIO pins as outputs
GPIO.setup(AC_RELAY_PIN, GPIO.OUT)
GPIO.setup(HEAT_RELAY_PIN, GPIO.OUT)
GPIO.setup(FAN_HIGH_RELAY_PIN, GPIO.OUT)
GPIO.setup(FAN_LOW_RELAY_PIN, GPIO.OUT)

# Function to turn on AC
def turn_on_ac():
    GPIO.output(AC_RELAY_PIN, GPIO.LOW)  # Relays are often active low
    print("AC ON")

# Function to turn off AC
def turn_off_ac():
    GPIO.output(AC_RELAY_PIN, GPIO.HIGH)
    print("AC OFF")

# Function to turn on heat
def turn_on_heat():
    GPIO.output(HEAT_RELAY_PIN, GPIO.LOW)
    print("HEAT ON")

# Function to turn off heat
def turn_off_heat():
    GPIO.output(HEAT_RELAY_PIN, GPIO.HIGH)
    print("HEAT OFF")

# Function to turn on high speed fan
def turn_on_fan_high():
    GPIO.output(FAN_HIGH_RELAY_PIN, GPIO.LOW)
    GPIO.output(FAN_LOW_RELAY_PIN, GPIO.HIGH) #ensure low is off
    print("FAN HIGH")

# Function to turn on low speed fan
def turn_on_fan_low():
    GPIO.output(FAN_LOW_RELAY_PIN, GPIO.LOW)
    GPIO.output(FAN_HIGH_RELAY_PIN, GPIO.HIGH) #ensure high is off
    print("FAN LOW")

# Function to turn off fan
def turn_off_fan():
    GPIO.output(FAN_HIGH_RELAY_PIN, GPIO.HIGH)
    GPIO.output(FAN_LOW_RELAY_PIN, GPIO.HIGH)
    print("FAN OFF")

# Example usage (replace with your temperature control logic)
try:
    # Initialize all relays to off
    turn_off_ac()
    turn_off_heat()
    turn_off_fan()

    # Example: Turn on AC for 5 seconds, then turn on heat for 5 seconds
    turn_on_ac()
    time.sleep(5)
    turn_off_ac()

    turn_on_heat()
    time.sleep(5)
    turn_off_heat()

    turn_on_fan_high()
    time.sleep(5)
    turn_off_fan()

    turn_on_fan_low()
    time.sleep(5)
    turn_off_fan()

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    # Clean up GPIO settings
    turn_off_ac()
    turn_off_heat()
    turn_off_fan()
    GPIO.cleanup()
    print("GPIO cleaned up")