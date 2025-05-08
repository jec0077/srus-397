# Smart Room Utility System (SRUS)

The Smart Room Utility System (SRUS) is an embedded, Raspberry Pi–based project designed to monitor and control environmental conditions within a room using real-time sensor data and computer vision. The system integrates temperature and humidity sensors (AM2320), GPIO-controlled relays, and a Raspberry Pi camera running a YOLOv8 object detection model to automate utility decisions like activating air conditioning, heating, and ventilation based on occupancy and climate conditions.

The software architecture is modular, split into separate Python files for sensor interaction (sensors.py), relay control (relay.py), computer vision (camera.py), and data logging (data.py). A threading system (thread.py) ensures that the sensor and camera modules operate concurrently, allowing real-time monitoring and response without delay or conflict. Sensor readings are recorded and evaluated against user-defined thresholds, triggering appropriate actions such as turning on the fan if humidity rises or activating the AC if the temperature exceeds a certain level. Simultaneously, the computer vision system counts the number of people in the room to track occupancy and prevent overcapacity.

The project emphasizes real-time system coordination, energy efficiency, and embedded software design. Through modular coding, team collaboration, and performance testing, SRUS showcases how low-cost computing platforms can support intelligent, automated environmental control solutions suitable for smart buildings and classrooms.

University of Illinois-Chicago (UIC)
College of Engineering (COE)
Department of Electrical and Computer Engineering (ECE)
Team Engin33ring Knights (ECE.33)
Academic Year 2024-2025
