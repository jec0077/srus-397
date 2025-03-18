import sys
import cv2
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
    main={"size": (800, 480), "format": "RGB888"},
    controls={"FrameRate": 30}  # Higher FPS for smoother video
)
picam2.configure(camera_config)
picam2.start()

print("[INFO] Camera started... Press 'q' to exit.")

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
