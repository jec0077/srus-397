import cv2
from ultralytics import YOLO

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

    cv2.imshow("Person Detection (Conf ≥ 0.7)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
