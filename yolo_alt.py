import sys
import cv2
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2
import data

if len(sys.argv) < 4:
    print("Usage: python script.py <room_capacity> <room temperature> <room humidity>")
    sys.exit(1)

filename = "stats.txt"
rm_cap = int(sys.argv[1])
rm_temp = int(sys.argv[2])
rm_hum = int(sys.argv[3])
MyRoom = data.RoomInfo(rm_cap, rm_temp, rm_hum)

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Initialize Picamera2
picam2 = Picamera2()

# Set the camera configuration for preview
camera_config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
picam2.configure(camera_config)
picam2.start()

while True:
    # Capture the frame from the camera
    frame = picam2.capture_array()

    # Convert from RGB to BGR (OpenCV uses BGR format)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Run YOLO detection
    results = model(frame)

    for r in results:
        # Filter only persons (class 0) with confidence >= 0.7
        person_detections = r.boxes[(r.boxes.cls == 0) & (r.boxes.conf >= 0.7)]
        r.boxes = person_detections
        frame = r.plot()  # Draw filtered boxes

        # Display total persons detected
        cv2.putText(frame, f'Total Persons Detected: {len(r.boxes)} / {rm_cap}', 
                    (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)

    # Show the frame with detections
    cv2.imshow("Person Detection (Confidence >= 0.7)", frame)

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup and release resources
cv2.destroyAllWindows()
picam2.stop()
