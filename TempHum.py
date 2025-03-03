import time
import board
import busio
import adafruit_am2320

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

print("Scanning I2C bus...")
while not i2c.try_lock():
    pass  # Wait for the I2C bus to be ready

devices = i2c.scan()  # Scan devices to wake up AM2320
print(f"Detected I2C devices: {devices}")
i2c.unlock()

# Manually wake up the sensor: Some sensors need extra time
time.sleep(5)  # Give the sensor a full 5 seconds to wake up

try:
    sensor = adafruit_am2320.AM2320(i2c)
    print("Sensor initialized!")
except ValueError:
    print("Error: AM2320 sensor not found on I2C bus.")
    exit()
except Exception as e:
    print(f"Error initializing sensor: {e}")
    exit()

# Manually wake up the sensor: Some sensors need extra time
time.sleep(5)  # Give the sensor a full 5 seconds to wake up

# Read sensor data in loop
while True:
    try:
        temp_c = sensor.temperature  # Read temperature (�C)
        temp_f = (temp_c * 9 / 5) + 32  # Convert to �F
        time.sleep(4)
        humidity = sensor.relative_humidity  # Read humidity
        time.sleep(4)
        print(f"Temperature: {temp_c:.2f}�C / {temp_f:.2f}�F")
        print(f"Humidity: {humidity:.2f}%")

    except OSError as e:
        print(f"Error reading sensor data (OSError): {e}")
    except Exception as e:
        print(f"Error reading sensor data: {e}")

<<<<<<< HEAD
    time.sleep(3)  # Wait 2 seconds before next reading
=======
#    time.sleep(5)  # Wait 5 seconds before next reading
>>>>>>> 627710963405a31ebc19ff11ae2f1745efd1960b


