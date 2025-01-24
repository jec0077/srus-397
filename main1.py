# can detect faces within 30 inches, 

import cv2
import sys

# Check if the user provided the Haar cascade file path
if len(sys.argv) < 2:
    print("Usage: python script.py <haarcascade_file_path>")
    sys.exit(1)

cascPath = sys.argv[1]

# Load the Haar cascade file
faceCascade = cv2.CascadeClassifier(cascPath)
if faceCascade.empty():
    print(f"Error: Failed to load Haar cascade file from {cascPath}")
    sys.exit(1)

# Start video capture
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Could not open video capture.")
    sys.exit(1)

print("Press 'q' to quit the video stream.")

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    if not ret:
        print("Error: Failed to capture video frame.")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    print("! Display Frame")
    cv2.imshow('Video', frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("! Quit")
        break

# Release the video capture and close all windows
video_capture.release()
cv2.destroyAllWindows()