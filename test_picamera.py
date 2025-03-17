from picamera2 import Picamera2
from ultralytics import YOLO

try:
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)  # Adjust size as needed
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    # Release the picamera2 and close all windows
    picam2.stop()
    picam2.close()
    print("picamera2 imported successfully")
    picam2.close()
except Exception as e:
    print(f"Error: {e}")