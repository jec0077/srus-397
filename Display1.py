import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sensor data provider ? REPLACE this with your actual sensor interface
def get_sensor_data():
    temperature = random.uniform(22.5, 27.5)
    humidity = random.uniform(40, 60)
    air_quality = random.uniform(350, 800)  # ppm
    energy = random.randint(90, 160)
    return temperature, humidity, air_quality, energy

# Main UI setup
root = tk.Tk()
root.title("Smart Room UI")
root.geometry("800x480")
root.configure(bg="black")

# Load background
bg_image = Image.open("background.png").resize((800, 480))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load icons
icon_temp = ImageTk.PhotoImage(Image.open("temp.png").resize((50, 50)))
icon_air = ImageTk.PhotoImage(Image.open("air.png").resize((50, 50)))
icon_energy = ImageTk.PhotoImage(Image.open("energy.png").resize((50, 50)))

# Time & Date
time_label = tk.Label(root, font=("Helvetica", 44), fg="white", bg="black")
time_label.place(x=30, y=20)

date_label = tk.Label(root, font=("Helvetica", 20), fg="white", bg="black")
date_label.place(x=30, y=80)

# Sensor Labels
tk.Label(root, image=icon_temp, bg="black").place(x=30, y=140)
temp_label = tk.Label(root, font=("Helvetica", 28), fg="lightgreen", bg="black")
temp_label.place(x=100, y=145)

tk.Label(root, image=icon_air, bg="black").place(x=30, y=200)
air_label = tk.Label(root, font=("Helvetica", 24), fg="orange", bg="black")
air_label.place(x=100, y=210)

tk.Label(root, image=icon_energy, bg="black").place(x=30, y=260)
energy_label = tk.Label(root, font=("Helvetica", 24), fg="cyan", bg="black")
energy_label.place(x=100, y=270)

# Energy Chart
energy_data = [100] * 10
fig = Figure(figsize=(3.5, 1.8), dpi=100)
ax = fig.add_subplot(111)
line, = ax.plot(energy_data, color='yellow')
ax.set_ylim(0, 300)
ax.set_title("Energy Usage")
ax.set_facecolor("black")
ax.title.set_color("white")
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=400, y=180)

# Update Functions
def update_time():
    now = datetime.now()
    time_label.config(text=now.strftime("%H:%M"))
    date_label.config(text=now.strftime("%Y-%m-%d"))
    root.after(1000, update_time)

def update_data():
    temperature, humidity, air_quality, energy = get_sensor_data()
    temp_label.config(text=f"{temperature:.1f}�C")
    air_label.config(text=f"{air_quality:.0f} ppm")
    energy_label.config(text=f"{energy} W")

    # Update chart
    energy_data.append(energy)
    if len(energy_data) > 10:
        energy_data.pop(0)
    line.set_ydata(energy_data)
    line.set_xdata(range(len(energy_data)))
    ax.set_xlim(0, len(energy_data))
    canvas.draw()

    root.after(5000, update_data)

# Start updates
update_time()
update_data()
root.mainloop()
