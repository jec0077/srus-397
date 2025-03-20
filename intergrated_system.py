#Date:10/20/2025
#Shishir Pokharel
#SRUS team33
# integrated_system.py

import threading
import time
import datetime
import cv2
import matplotlib.pyplot as plt

# Import your modules (do not modify their internal code)
import AQsensor       # Air quality monitoring
import TempHum        # Temperature & Humidity monitoring (this logs data via data.py)
import relay          # Relay control functions
import data           # Data logging and room info
import display        # Display GUI (if desired; note this runs its own Tkinter mainloop)
from ultralytics import YOLO
from picamera2 import Picamera2

# Global shared variables and locks
people_count_lock = threading.Lock()
people_count = 0
occupancy_log = []      # List of tuples: (timestamp, average_people_count)
relay_usage = {"AC": 0, "Heat": 0, "FanHigh": 0, "FanLow": 0}  # in seconds
relay_usage_lock = threading.Lock()

# Configuration parameters
ROOM_CAPACITY = 10          # Default room capacity (can be passed as arg)
TARGET_TEMP_F = 75.0        # Default room temperature in Fahrenheit
OCCUPANCY_THRESHOLD_HIGH = 0.8 * ROOM_CAPACITY  # When occupancy is high, cool more
OCCUPANCY_THRESHOLD_LOW = 0.5 * ROOM_CAPACITY   # When occupancy is low, allow warmer temperature
CONTROL_INTERVAL = 60       # Seconds between temperature control decisions
DATA_LOG_INTERVAL = 3600    # Log occupancy every hour
ENERGY_RATE_AC = 3.5        # Example: AC power rating in kW
ENERGY_RATE_HEAT = 4.0      # Example: Heater power rating in kW

# Create a RoomInfo instance for logging sensor conditions (using defaults or overrides)
MyRoom = data.RoomInfo(capacity=ROOM_CAPACITY, temperature=TARGET_TEMP_F, humidity=60.0)

# ----------------------------
# Thread: Person Detection
# ----------------------------
def person_detection_thread():
    """
    Runs YOLO-based person detection using Picamera2.
    Updates the global people_count variable.
    """
    global people_count

    # Load YOLOv8 model (using your alternative module yolo_alt logic from main.py)
    # For integration we use YOLO from ultralytics directly.
    model = YOLO("yolov8n.pt")
    
    # Initialize camera
    picam2 = Picamera2()
    camera_config = picam2.create_video_configuration(
        main={"size": (800, 480), "format": "RGB888"},
        controls={"FrameRate": 30}
    )
    picam2.configure(camera_config)
    picam2.start()
    
    print("[Person Detection] Camera started...")
    
    try:
        while True:
            frame = picam2.capture_array()
            results = model(frame, verbose=False)
            
            count_in_frame = 0
            for r in results:
                # Filter for 'person' class (class id 0) with confidence >= 0.7
                person_detections = r.boxes[r.boxes.cls == 0]
                person_detections = person_detections[person_detections.conf >= 0.7]
                count_in_frame += len(person_detections)
                # Optionally, draw bounding boxes on frame if needed:
                frame = r.plot()
            
            # Update global people count (thread-safe)
            with people_count_lock:
                people_count = count_in_frame
            
            # Also overlay the count on the frame for visualization if desired.
            cv2.putText(frame, f'Total Persons: {count_in_frame} / {ROOM_CAPACITY}', 
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            cv2.imshow("Person Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            
            # Sleep briefly before processing next frame
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("[Person Detection] Interrupted by user.")
    finally:
        cv2.destroyAllWindows()
        picam2.stop()
        print("[Person Detection] Camera stopped.")

# ----------------------------
# Thread: Temperature Control
# ----------------------------
def temperature_control_thread():
    """
    Adjusts room temperature automatically based on the current number of people.
    Uses relay functions to control AC/Heat and logs relay active time.
    """
    global TARGET_TEMP_F
    last_control_time = time.time()
    
    while True:
        current_time = time.time()
        elapsed = current_time - last_control_time
        last_control_time = current_time

        # Retrieve current occupancy (thread-safe)
        with people_count_lock:
            current_people = people_count
        
        # Decide target temperature based on occupancy:
        # (For example, if occupancy is high, lower target temperature)
        if current_people >= OCCUPANCY_THRESHOLD_HIGH:
            new_target = TARGET_TEMP_F - 2.0
        elif current_people <= OCCUPANCY_THRESHOLD_LOW:
            new_target = TARGET_TEMP_F + 2.0
        else:
            new_target = TARGET_TEMP_F  # maintain default
        
        # If new target is lower than current, assume room is too warm: turn on AC.
        # If new target is higher, assume room is too cool: turn on heat.
        # (This example logic is simplistic. In practice, you might compare sensor readings vs. target.)
        if new_target < TARGET_TEMP_F:
            relay.turn_on_ac()
            # Simulate relay usage time accumulation
            with relay_usage_lock:
                relay_usage["AC"] += elapsed
            time.sleep(5)  # Allow time for cooling to take effect
            relay.turn_off_ac()
        elif new_target > TARGET_TEMP_F:
            relay.turn_on_heat()
            with relay_usage_lock:
                relay_usage["Heat"] += elapsed
            time.sleep(5)
            relay.turn_off_heat()
        else:
            # If no change is needed, ensure both systems are off.
            relay.turn_off_ac()
            relay.turn_off_heat()
        
        # Update target for logging (and for the next cycle)
        TARGET_TEMP_F = new_target
        
        # Optionally log the action (using data.py)
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.ping_message_to_file("room.txt", f"Temperature adjusted to {TARGET_TEMP_F:.2f}°F based on occupancy {current_people}")
        
        time.sleep(CONTROL_INTERVAL)

# ----------------------------
# Thread: Sensor Monitoring
# ----------------------------
def sensor_monitoring_thread():
    """
    Runs the temperature/humidity sensor loop from TempHum and the air quality sensor loop from AQsensor.
    For integration purposes, we run these loops sequentially in this thread.
    (They each log their output to the file and print status.)
    """
    # Run the TempHum loop in a separate thread if needed.
    # Here, we simulate one cycle every 15 seconds.
    while True:
        try:
            # Temperature & Humidity cycle:
            # (The TempHum module already writes to file via MyRoom.temp_cond_met and hum_cond_met.)
            # For our integration, we simply call a single cycle.
            sensor = TempHum  # using the module's logic implicitly; in practice you may want to call a function.
            # We assume the TempHum.py script is running separately. If not, you could import and call a function here.
            # (For this integration, we just sleep to simulate sensor reading intervals.)
            time.sleep(15)
            
            # Air quality sensor cycle:
            # We assume the AQsensor module is running its own infinite loop if called directly.
            # If you wish to run it concurrently, you could launch AQsensor.main() in a thread.
            # Here, for demonstration, we sleep.
            time.sleep(15)
            
        except KeyboardInterrupt:
            break

# ----------------------------
# Thread: Data Logging
# ----------------------------
def data_logging_thread():
    """
    Every hour, record the current people count (averaged over the hour) into occupancy_log.
    """
    hour_readings = []
    next_log_time = time.time() + DATA_LOG_INTERVAL
    
    while True:
        current_time = time.time()
        with people_count_lock:
            hour_readings.append(people_count)
        
        if current_time >= next_log_time:
            # Compute average occupancy for the past hour
            avg_occ = sum(hour_readings) / len(hour_readings) if hour_readings else 0
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            occupancy_log.append((timestamp, avg_occ))
            # Also log to file using data.py
            data.ping_message_to_file("room.txt", f"Average occupancy in last hour: {avg_occ:.2f}")
            # Reset for next hour
            hour_readings = []
            next_log_time = current_time + DATA_LOG_INTERVAL
        
        time.sleep(10)  # sample every 10 seconds

# ----------------------------
# Main Integration Function
# ----------------------------
def main():
    # Start threads for each subsystem
    threads = []
    
    # Person detection thread
    t1 = threading.Thread(target=person_detection_thread, name="PersonDetection")
    threads.append(t1)
    
    # Temperature control thread
    t2 = threading.Thread(target=temperature_control_thread, name="TempControl")
    threads.append(t2)
    
    # Sensor monitoring thread
    t3 = threading.Thread(target=sensor_monitoring_thread, name="SensorMonitor")
    threads.append(t3)
    
    # Data logging thread
    t4 = threading.Thread(target=data_logging_thread, name="DataLogger")
    threads.append(t4)
    
    # (Optional) You can also run the display GUI in its own thread if you wish
    # t5 = threading.Thread(target=display.main, name="DisplayGUI")
    # threads.append(t5)
    
    for t in threads:
        t.daemon = True  # Ensure threads exit when main program exits
        t.start()
    
    print("[Main] All subsystem threads started. Press Ctrl+C to exit.")
    
    try:
        # Keep the main thread alive.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[Main] Exiting... Generating charts and energy usage report.")
        generate_reports()

def generate_reports():
    """
    Generates charts for occupancy and prints an energy usage estimation report.
    """
    # Generate occupancy chart
    if occupancy_log:
        timestamps, occ_values = zip(*occupancy_log)
        # Convert timestamps to datetime objects for plotting
        dt_timestamps = [datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in timestamps]
        
        plt.figure(figsize=(10, 5))
        plt.plot(dt_timestamps, occ_values, marker='o')
        plt.title("Hourly Average Occupancy")
        plt.xlabel("Time")
        plt.ylabel("People Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("occupancy_chart.png")
        plt.show()
        print("[Report] Occupancy chart saved as occupancy_chart.png.")
    else:
        print("[Report] No occupancy data to generate chart.")
    
    # Energy usage estimation report (using cumulative relay active times)
    with relay_usage_lock:
        ac_time_hours = relay_usage["AC"] / 3600.0
        heat_time_hours = relay_usage["Heat"] / 3600.0
    
    energy_ac = ac_time_hours * ENERGY_RATE_AC  # in kWh
    energy_heat = heat_time_hours * ENERGY_RATE_HEAT  # in kWh
    
    print("\n[Energy Usage Report]")
    print(f"AC ran for {ac_time_hours:.2f} hours, estimated energy usage: {energy_ac:.2f} kWh")
    print(f"Heater ran for {heat_time_hours:.2f} hours, estimated energy usage: {energy_heat:.2f} kWh")
    
    # Optionally, write these details to a file
    with open("energy_report.txt", "w") as report_file:
        report_file.write("[Energy Usage Report]\n")
        report_file.write(f"AC run time: {ac_time_hours:.2f} hours, Energy: {energy_ac:.2f} kWh\n")
        report_file.write(f"Heater run time: {heat_time_hours:.2f} hours, Energy: {energy_heat:.2f} kWh\n")
    print("[Report] Energy usage report saved as energy_report.txt.")

if __name__ == "__main__":
    main()
