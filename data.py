"""
---------------------------------------------------------
Filename: data.py
Description: This script <>
Author: Josh Campbell <jcampb36@uic.edu>,
        Aaron Tillery <atill4@uic.edu>
Date Created: 2025-01-23
Last Modified: 2025-02-10
Version: 1.0
Python Version: 3.11.1

Dependencies:
    - datetime
    - time

Usage:
    - <>

Example:
    - <>
---------------------------------------------------------
"""
# Import dependent libraries
import datetime
import time
import relay

def create_data_file(filename: str) -> bool:
    """Creates a data file and writes initial room condition data."""
    
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

def ping_message_to_file(filename: str, message: str):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message_content = (
        f"Message Ping at {now_time}"
        f"\t{message}"
        ". . . .\n\n"
    )
    
    try:
        with open(filename, "a") as _file:
            _file.write(message_content)
    except Exception as e:
        print(f"Error appending file '{filename}': {e}")


class RoomInfo:
    """Represents room preferences such as owner, capacity, temperature, and humidity."""

    def __init__(self, owner: str = "* <>", capacity: int = 10, temperature: float = 75.0, humidity: float = 60.0):
        """
        Initializes a RoomInfo instance.
        
        :param owner: Room owner's name and contact (default: "* <>").
        :param capacity: Preferred room capacity (default: 10).
        :param temperature: Preferred temperature in Fahrenheit (default: 75.0°F).
        :param humidity: Preferred humidity percentage (default: 60.0%).
        """
        self.room_owner = owner
        self.room_cap = capacity
        self.room_temp = temperature
        self.room_hum = humidity

    def __str__(self):
        """Returns a string representation of the room details."""
        return (f"Room Owner: {self.room_owner}\n"
                f"Preferred Capacity: {self.room_cap}\n"
                f"Preferred Temperature: {self.room_temp}oF\n"
                f"Preferred Humidity: {self.room_hum}%")

    def get_room_data(self) -> list:
        return [self.room_cap, self.room_temp, self.room_hum]
    
    def rm_cap_met(self, filename: str, cap_var: int) -> bool:
        """
        Checks if the room is over capacity and logs it if necessary.

        :param filename: File to log the warning.
        :param cap_var: Current room occupancy.
        :return: True if room is over capacity, False otherwise.
        """
        if cap_var > self.room_cap:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(filename, "a") as _file:
                _file.write(f"{now_time}\tRoom is over capacity ({cap_var} / {self.room_cap})\n")
                _file.write("\t! Contacting Room Owner\n")
                _file.write(". . . .\n")
            time.sleep(0.1)
            relay.turn_off_heat()
            return True
        relay.turn_on_heat()
        return False

    def temp_cond_met(self, filename: str, temp_var: float) -> bool:
        """
        Checks if the room temperature is outside the preferred range and logs it if necessary.

        :param filename: File to log the warning.
        :param temp_var: Current room temperature.
        :return: True if room temperature is out of range, False otherwise.
        """
        threshold = 2.0  # Allow 2°F tolerance

        if abs(temp_var - self.room_temp) < threshold:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(filename, "a") as _file:
                _file.write(f"{now_time}\tRoom temperature out of range ({temp_var:.2f}°F)\n")
                _file.write("\t! Contacting Room Owner\n")
                _file.write(". . . .\n")
            time.sleep(0.1)
            relay.turn_on_ac()
            return True
        relay.turn_off_ac()
        return False

    def hum_cond_met(self, filename: str, hum_var: float) -> bool:
        """
        Checks if the room humidity is outside the preferred range and logs it if necessary.

        :param filename: File to log the warning.
        :param hum_var: Current room humidity.
        :return: True if room humidity is out of range, False otherwise.
        """
        threshold = 5.0  # Allow 5% tolerance

        if abs(hum_var - self.room_hum) < threshold:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(filename, "a") as _file:
                _file.write(f"{now_time}\tRoom humidity out of range ({hum_var:.2f}%)\n")
                _file.write("\t! Contacting Room Owner\n")
                _file.write(". . . .\n")
            time.sleep(0.1)
            relay.turn_on_fan_high()
            return True
        relay.turn_off_heat()
        return False
    
    def change_room_instance(self, owner: str = None, capacity: int = None, temperature: float = None, humidity: float = None):
        """
        Updates the room instance with new values while keeping defaults if no new values are provided.

        :param owner: New room owner's name and contact (default: existing value).
        :param capacity: New preferred room capacity (default: existing value).
        :param temperature: New preferred temperature in Fahrenheit (default: existing value).
        :param humidity: New preferred humidity percentage (default: existing value).
        """
        if owner is not None:
            self.room_owner = owner
        if capacity is not None:
            self.room_cap = capacity
        if temperature is not None:
            self.room_temp = temperature
        if humidity is not None:
            self.room_hum = humidity


if __name__ == "__main__":
    pass