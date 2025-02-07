"""
---------------------------------------------------------
Filename: sensors.py
Description: This script <>
Author: Josh Campbell <jcampb36@uic.edu>,
        Aaron Tillery <atill4@uic.edu>
Date Created: 2025-01-28
Last Modified: 2025-02-07
Version: 0.1
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
import random

# Testing randomized numbers between 20 degrees Celsius and 25 degrees Celsius
celsius_var = random.uniform(20.00, 25.00)

# Converting the Celsius numbers into Fahrenheit
fahrenheit_var = (celsius_var * 9.00 / 5.00) + 32.00

# Testing print statement to see if randomized variables work
print(f"{round(celsius_var, 2)} degree Celsius is equal to {round(fahrenheit_var, 2)} degree Fahrenheit.")

if __name__ == "__main__":
    MyRoom = data.RoomInfo("Josh Campbell <jcampb36@uic.edu>", 5, 74.0, 55.0) # see RoomInfo class in data.py