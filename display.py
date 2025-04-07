import tkinter as tk
from tkinter import ttk
import random
import camera  # Assuming this provides MyData = [people_count, temp, humidity]

# Function to get sensor data
def get_sensor_data():
    try:
        data_arr = camera.MyData.get_room_data()  # Simulated data retrieval
        people_count = data_arr[0]
        temp = data_arr[1]
        humidity = data_arr[2]

        temp_label.config(text=f"Temperature: {temp:.1f}oF")
        humidity_label.config(text=f"Humidity: {humidity:.1f}%")
        people_label.config(text=f"People in Room: {people_count}")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

    root.after(3000, get_sensor_data)  # Update every 3 seconds

# Function to adjust temperature manually
def adjust_temp(value):
    temp_label.config(text=f"Temperature: {float(value):.1f}oF")

def main():
    global root, people_label, temp_label, humidity_label, status_label

    # GUI Setup
    root = tk.Tk()
    root.title("Smart Room Display")
    root.geometry("800x480")
    root.configure(bg="white")

    # Header
    header = tk.Label(root, text="Smart Room Monitor", font=("Arial", 18, "bold"), bg="blue", fg="white")
    header.pack(fill="x")

    # Sensor Readings
    temp_label = tk.Label(root, text="Temperature: --°C", font=("Arial", 16), bg="white")
    temp_label.pack(pady=5)

    humidity_label = tk.Label(root, text="Humidity: --%", font=("Arial", 16), bg="white")
    humidity_label.pack(pady=5)

    people_label = tk.Label(root, text="People in Room: --", font=("Arial", 16), bg="white")
    people_label.pack(pady=5)

    # Temperature Adjustment
    temp_adjust_frame = tk.Frame(root, bg="white")
    temp_adjust_frame.pack(pady=10)

    tk.Label(temp_adjust_frame, text="Adjust Temp:", font=("Arial", 14), bg="white").pack(side="left")
    temp_slider = ttk.Scale(temp_adjust_frame, from_=30, to=90, orient="horizontal", command=adjust_temp)
    temp_slider.pack(side="left", padx=10)

    # Status
    status_label = tk.Label(root, text="System Running...", font=("Arial", 12), bg="white", fg="green")
    status_label.pack(pady=5)

    # Start Sensor Data Update
    get_sensor_data()

    # Run the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
