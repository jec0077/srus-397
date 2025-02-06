"""
---------------------------------------------------------
Filename: sensors.py
Description: This script <>
Author: Josh Campbell <jcampb36@uic.edu>,
        Aaron Tillery <atill4@uic.edu>
Date Created: 2025-01-28
Last Modified: 2025-02-05
Version: 0.1
Python Version: 3.11.1

Dependencies:
    - <>

Usage:
    - <>

Example:
    - <>
---------------------------------------------------------
"""
# Import dependent libraries
import data
import random

celsius = random.uniform(20.0,24.44) #Testing randomized numbers between 20 degree celsisus and 24.444 degree celsisus

fahrenheit = (celsius * 9/5) + 32 #Converting the Celsisus numbers into Fahrenheit

print(str(celsius )+ " degree Celsisus is equal to " + str(fahrenheit )+ " degree Fahrenheit.") #Testing print statment to see if ramdonized variables work



