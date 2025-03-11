import cv2
import sys
from ultralytics import YOLO

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

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    for r in results:
        # Filter only persons (class 0) with confidence >= 0.7
        person_detections = r.boxes[(r.boxes.cls == 0) & (r.boxes.conf >= 0.7)]
        r.boxes = person_detections
        frame = r.plot()  # Draw filtered boxes

        cv2.putText(frame, f'Total Persons Detected: {len(r.boxes)} / {rm_cap}', (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)

    cv2.imshow("Person Detection (Confidence >= 0.7)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
