"""
---------------------------------------------------------
Filename: data.py
Description: This script <>
Author: Josh Campbell <jcampb36@uic.edu>,
        Aaron Tillery <atill4@uic.edu>
Date Created: 2025-01-23
Last Modified: 2025-01-24
Version: 0.1
Python Version: 3.11.1

Dependencies:
    - time

Usage:
    - <>

Example:
    - <>
---------------------------------------------------------
"""
# Import dependent libraries
import datetime

now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_data_file(filename: str) -> bool:
    """Creates a data file and writes initial room condition data."""
    
    initial_content = (
        "Room Condition Data\n"
        f"Filename: {filename}\n"
        f"Collected: {now_time}\n"
        ". . . .\n\n"
    )

    try:
        with open(filename, "w") as _file:
            _file.write(initial_content)
        return True
    except Exception as e:
        print(f"Error creating file '{filename}': {e}")
        return False
        
        
def temp_cond_met(temp_var: int, temp_set: int) -> bool:
    pass

def rm_cap_met(filename: str, cap_var: int, cap_set: int)-> bool:
    if (cap_var > cap_set):
        with open(filename, "a") as _file:
            _file.write(f"{now_time}\tRoom is over capacity ({cap_var} / {cap_set})\n")
            _file.write(f"\t! Contacting Room Owner\n")
            _file.write(f". . . .\n")
    else:
        pass

def hum_cond_met(hum_var: int, hum_set: int) -> bool:
    pass