"""
---------------------------------------------------------
Filename: main.py
Description: This script captures video from the default camera
    and detects faces in real-time using a Haar cascade classifier.
    The detected faces are highlighted with rectangles and the total
    number of detected faces is displayed on the screen.
Author: Josh Campbell <jcampb36@uic.edu>,
        Aaron Tillery <atill4@uic.edu>
Date Created: 2024-11-29
Last Modified: 2025-01-28
Version: 1.0
Python Version: 3.11.1

Dependencies:
    - cv2 (opencv-python)
    - sys

Usage:
    - Run the script from the command line with the path to a Haar cascade XML file:
        python main.py <haarcascade_file_path>
    - The script will display the video feed from your webcam, with rectangles
        drawn around any detected faces. Press 'q' to quit.

Example:
    - python main.py haarcascade_frontalface_default.xml
    - This will start the face detection with the specified Haar cascade classifier file.
---------------------------------------------------------
"""

# Import dependent libraries
import cv2
import sys

# Import local libraries
import data
import sensors


# Check if the user provided the Haar cascade file path
if len(sys.argv) < 2:
    print("Usage: python script.py <haarcascade_file_path>")
    sys.exit(1)

cascPath = sys.argv[1]
rmCap = int(sys.argv[2])

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
    num_of_persons = 0
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        num_of_persons += 1

    # Display the resulting frame
    # print("! Display Frame")
    cv2.putText(frame, f'Total Persons Detected: {num_of_persons} / {rmCap}', (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    # TODO: Configure Data module for num_of_persons
    data.take_data_count(num_of_persons, rmCap)
    cv2.imshow('Video', frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("! Quit")
        break

# Release the video capture and close all windows
video_capture.release()
cv2.destroyAllWindows()