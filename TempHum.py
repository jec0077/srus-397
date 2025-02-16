import time
import board
import busio
import adafruit_am2320

# Initialize I2C bus (gpio)
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize AM2320 sensor
sensor = adafruit_am2320.AM2320(i2c)

while True:
    try:
        # Read temperature in Celsius
        temp_c = sensor.temperature
        # Convert to Fahrenheit
        temp_f = (temp_c * 9/5) + 32
        # Read humidity
        humidity = sensor.relative_humidity

        # Print values
        print(f"Temperature: {temp_c:.2f}°C / {temp_f:.2f}°F")
        print(f"Humidity: {humidity:.2f}%")

    except Exception as e:
        print(f"Error: {e}")

    # Delay before next reading
    time.sleep(2)
