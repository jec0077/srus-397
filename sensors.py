"""
---------------------------------------------------------
Filename: sensors.py
Description: This script <>
Author: Josh Campbell <jcampb36@uic.edu>,
        Aaron Tillery <atill4@uic.edu>
Date Created: 2025-01-28
Last Modified: 2025-02-10
Version: 0.2
Python Version: 3.11.1

Dependencies:
    - random
    
Usage:
    - <>

Example:
    - <>
---------------------------------------------------------
"""
# Import dependent libraries
import data

# TODO: I2C bus GPIO pin configuration

# Initialize of bus and sensor

# While . . .

if __name__ == "__main__":
    # TESTING
    if True:
        pass
    
    # File and Room testing
    data.create_data_file("stats.txt")
    MyRoom = data.RoomInfo("Josh Campbell <jcampb36@uic.edu>", 5, 60.0, 55.0) # see RoomInfo class in data.py
    print(f"MyRoom:\n{MyRoom}\n. . .")