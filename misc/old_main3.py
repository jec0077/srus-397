# NOT IN USE

import cv2
import imutils

# Initializing the HOG person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Open the webcam (0 is the default webcam)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Reading the video stream from the webcam
    ret, image = cap.read()
    if ret:
        # Resize the image for better performance
        image = imutils.resize(image, width=min(400, image.shape[1]))

        # Detecting all the regions in the image that contain pedestrians
        (regions, _) = hog.detectMultiScale(image,
                                           winStride=(4, 4),
                                           padding=(4, 4),
                                           scale=1.05)

        # Drawing the regions (bounding boxes) around detected pedestrians
        for (x, y, w, h) in regions:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Displaying the output image
        cv2.imshow("Webcam Feed", image)

        # Press 'q' to exit the loop and close the webcam feed
        if cv2.waitKey(3) & 0xFF == ord('q'):
            break
    else:
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
