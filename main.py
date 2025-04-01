# integrate yolo, temphum, relay
# second prime aqs, display

import sys
import cv2
import time

# import libcamera
from ultralytics import YOLO
from picamera2 import Picamera2

import board
import busio
import adafruit_am2320

import yolo_alt
import data
import relay
import TempHum
import AQsensor
import display

def main():
    # Read input arguments
    rm_cap = int(sys.argv[1])
    rm_temp = float(sys.argv[2])
    rm_hum = float(sys.argv[3])
    MyRoom = data.RoomInfo(rm_cap, rm_temp, rm_hum)
    data.create_data_file("room.txt")
    
    logic_break1 = 0
    logic_break2 = 0
    logic_break3 = 0

    # Load YOLOv8 model (Nano version for efficiency)
    model = yolo_alt.YOLO("yolov8n.pt")

    # Initialize Picamera2 with optimized settings
    picam2 = yolo_alt.Picamera2()
    camera_config = picam2.create_video_configuration(
        main={"size": (800, 480), "format": "RGB888"},
        controls={"FrameRate": 30}  # Higher FPS for smoother video
    )
    picam2.configure(camera_config)
    picam2.start()

    print("[INFO] Camera started... Press 'q' to exit.")
    
    i2c = busio.I2C(board.SCL, board.SDA)

    print("Scanning I2C bus...")
    while not i2c.try_lock():
        pass  # Wait for the I2C bus to be ready

    devices = i2c.scan()  # Scan devices to wake up AM2320
    print(f"Detected I2C devices: {devices}")
    i2c.unlock()
    
    try:
        sensor = adafruit_am2320.AM2320(i2c)
        print("Sensor initialized!")
    except ValueError:
        print("Error: AM2320 sensor not found on I2C bus.")
        exit()
    except Exception as e:
        print(f"Error initializing sensor: {e}")
        exit()
        
    time.sleep(5)

    try:
        while True:
            # Capture frame
            frame = picam2.capture_array()

            # Run YOLO detection (efficient mode)
            results = model(frame, verbose=False)  # Disable verbose output

            for r in results:
                # Filter for 'person' class (0) with confidence >= 0.7
                person_detections = r.boxes[r.boxes.cls == 0]
                person_detections = person_detections[person_detections.conf >= 0.7]

                # Update the detections
                r.boxes = person_detections

                # Use YOLO's built-in `.plot()` method for optimized drawing
                frame = r.plot()

                # Display total person count
                cv2.putText(frame, f'Total Persons: {len(r.boxes)} / {rm_cap}', 
                            (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                
                # Read sensor data in loop
                temp_c = sensor.temperature  # Read temperature (oC)
                temp_f = (temp_c * 9 / 5) + 32  # Convert to oF
                humidity = sensor.relative_humidity  # Read humidity
                
                print(f"Temperature: {temp_c:.2f}oC / {temp_f:.2f}oF")
                print(f"Humidity: {humidity:.2f}%")
                
                if MyRoom.rm_cap_met("room.txt", len(r.boxes)) == True and logic_break1 == 0:
                    relay.turn_on_ac()
                    logic_break1 = 1
                elif logic_break1 == 1 and len(r.boxes) < rm_cap:
                    relay.turn_off_ac()
                    logic_break1 = 0
                    
                if MyRoom.hum_cond_met("room.txt", rm_hum) == True and logic_break2 == 0:
                    pass
                
                if MyRoom.temp_cond_met("room.txt", rm_temp) == True and logic_break3 == 0:
                    pass
                

            # Show frame in OpenCV window
            cv2.imshow("Person Detection - Picamera2", frame)

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    
    except KeyboardInterrupt:
        print("\n[INFO] Stopping camera...")

    finally:
        # Cleanup
        cv2.destroyAllWindows()
        picam2.stop()
        print("[INFO] Camera stopped.")
        quit()


if __name__ == "__main__":
    main()
