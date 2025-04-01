import time
import board
import busio
import adafruit_am2320

import data

def main():
    data.create_data_file("room.txt")
    MyRoom = data.RoomInfo(temperature=75.40, humidity=15.00)
    data.ping_message_to_file("room.txt", "Testing TempHum.py")

    # Initialize I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    print("Scanning I2C bus...")
    while not i2c.try_lock():
        pass  # Wait for the I2C bus to be ready

    devices = i2c.scan()  # Scan devices to wake up AM2320
    print(f"Detected I2C devices: {devices}")
    i2c.unlock()

    # Manually wake up the sensor: Some sensors need extra time
    time.sleep(4)  # Give the sensor a full 4 seconds to wake up

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
    time.sleep(4)  # Give the sensor a full 4 seconds to wake up

    # Read sensor data in loop
    while True:
        try:
            temp_c = sensor.temperature  # Read temperature (oC)
            temp_f = (temp_c * 9 / 5) + 32  # Convert to oF
            time.sleep(4)
            humidity = sensor.relative_humidity  # Read humidity
            time.sleep(4)
            print(f"Temperature: {temp_c:.2f}oC / {temp_f:.2f}oF")
            print(f"Humidity: {humidity:.2f}%")
            # MyRoom.temp_cond_met("room.txt", temp_f)
            # MyRoom.hum_cond_met("room.txt", humidity)

        except OSError as e:
            print(f"Error reading sensor data (OSError): {e}")
        except Exception as e:
            print(f"Error reading sensor data: {e}")

        time.sleep(4)  # Wait 4 seconds before next reading


if __name__ == "__main__":
    main()