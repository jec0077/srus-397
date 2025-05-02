from threading import Thread

from camera import main as camera_main
from sensors import main as sensors_main

thread_cam = Thread(target=camera_main)
thread_sens = Thread(target=sensors_main)

thread_cam.start()
thread_sens.start()

thread_cam.join()
thread_sens.join()