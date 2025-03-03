import cv2
import sys
from picamera2 import Picamera2
# import adafruit_ads1x15
# import AQsensor

# Check if the user provided the Haar cascade file path
if len(sys.argv) < 2:
    print("Usage: python script.py <haarcascade_file_path> <room_capacity>")
    sys.exit(1)

filename = "stats.txt"
cascPath = sys.argv[1]
rm_cap = int(sys.argv[2])

# Load the Haar cascade file
faceCascade = cv2.CascadeClassifier(cascPath)
if faceCascade.empty():
    print(f"Error: Failed to load Haar cascade file from {cascPath}")
    sys.exit(1)

# Initialize picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)  # Adjust size as needed
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

print("Press 'q' to quit the video stream.")
print("! Starting Video Stream")

# Create data file (assuming you have data.create_data_file)
# data.create_data_file(filename=filename)

curr_max_in_rm = [0, 0, 0]
num_of_persons = 0 #initialize the num of persons.

while True:
    # Capture frame-by-frame
    frame = picam2.capture_array()

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
    cv2.putText(frame, f'Total Persons Detected: {num_of_persons} / {rm_cap}', (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
<<<<<<< HEAD
   
    if (num_of_persons > curr_max_in_rm[0]):
        MyRoom.rm_cap_met("stats.txt", num_of_persons)
        curr_max_in_rm[0] = num_of_persons
    if (num_of_persons > curr_max_in_rm[1]):
        MyRoom.rm_cap_met("stats.txt", num_of_persons)
        curr_max_in_rm[1] = 0
    if (num_of_persons > curr_max_in_rm[2]):
        MyRoom.rm_cap_met("stats.txt", num_of_persons)
        curr_max_in_rm[2] = 0
    # TODO: Configure Data module for num_of_persons
=======
    # cv2.putText(frame, f'CO2: {}', (70, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    # AQsensor.main()
>>>>>>> eda7412838e9190fd285d5968d4298c3ae78bcc8
    
    if num_of_persons > curr_max_in_rm[0]:
        # MyRoom.rm_cap_met("stats.txt", num_of_persons) # add your room logic here.
        curr_max_in_rm[0] = num_of_persons
    if num_of_persons > curr_max_in_rm[1]:
        # MyRoom.rm_cap_met("stats.txt", num_of_persons) # add your room logic here.
        curr_max_in_rm[1] = num_of_persons
    if num_of_persons > curr_max_in_rm[2]:
        # MyRoom.rm_cap_met("stats.txt", num_of_persons) # add your room logic here.
        curr_max_in_rm[2] = num_of_persons

    cv2.imshow('Video', frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("! Quit")
        break

# Release the picamera2 and close all windows
picam2.stop()
picam2.close()
cv2.destroyAllWindows()
 # cd /home/team33/code/srus-397/
 # python main.py ./haarcascade_frontalface_default.xml 2