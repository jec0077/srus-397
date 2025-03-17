import sys
import cv2
import numpy as np
import time
from ultralytics import YOLO
from picamera2 import Picamera2
import data

# Ensure correct usage
if len(sys.argv) < 4:
    print("Usage: python script.py <room_capacity> <room_temperature> <room_humidity>")
    sys.exit(1)

# Read input arguments
rm_cap = int(sys.argv[1])
rm_temp = int(sys.argv[2])
rm_hum = int(sys.argv[3])
MyRoom = data.RoomInfo(rm_cap, rm_temp, rm_hum)

# Load YOLOv8 model (Nano version for efficiency)
model = YOLO("yolov8n.pt")

# Initialize Picamera2 with optimized settings
picam2 = Picamera2()
camera_config = picam2.create_video_configuration(
    main={"size": (1280, 720), "format": "RGB888"}  # Higher FPS for smoother video
)
picam2.configure(camera_config)
picam2.start()

print("[INFO] Camera started... Press 'q' to exit.")

# Frame skipping to improve speed
# frame_skip = 180  # Skips every second frame to improve performance
# frame_count = 0

try:
    while True:
        # start_time = time.time()  # Track time for FPS calculation

        # Capture frame
        frame = picam2.capture_array()

        # Ensure correct color representation
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  


        # Run YOLO detection (efficient mode)
        results = model(frame, stream=True)

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

        # Show frame in OpenCV window
        cv2.imshow("Person Detection - Picamera2", frame)

        # FPS Calculation
        # fps = 1 / (time.time() - start_time)
        # print(f"FPS: {fps:.2f}")

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # frame_count += 1  # Increment frame counter

except KeyboardInterrupt:
    print("\n[INFO] Stopping camera...")

finally:
    # Cleanup
    cv2.destroyAllWindows()
    picam2.stop()
    print("[INFO] Camera stopped.")
