from flask import Flask, request
import threading
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

sensor_data = {
    'humidity': [],
    'temperature': [],
    'soil_moisture': [],
    'timestamps': []
}

@app.route('/data', methods=['POST'])
def data():
    try:
        sensor_data['humidity'].append(float(request.form['humidity']))
        sensor_data['temperature'].append(float(request.form['temperature']))
        sensor_data['soil_moisture'].append(float(request.form['soilMoisture']))
        sensor_data['timestamps'].append(len(sensor_data['timestamps']) + 1)  # Simple timestamp
        
        update_gui()
        return 'Data received', 200
    except Exception as e:
        return str(e), 400

def update_gui():
    humidity_label.config(text=f"Humidity: {sensor_data['humidity'][-1]:.2f}%")
    temperature_label.config(text=f"Temperature: {sensor_data['temperature'][-1]:.2f} C")
    soil_moisture_label.config(text=f"Soil Moisture: {sensor_data['soil_moisture'][-1]:.2f}")

    update_graph()

def update_graph():
    ax.clear()
    ax.plot(sensor_data['timestamps'], sensor_data['humidity'], label='Humidity (%)', color='b')
    ax.plot(sensor_data['timestamps'], sensor_data['temperature'], label='Temperature (C)', color='r')
    ax.plot(sensor_data['timestamps'], sensor_data['soil_moisture'], label='Soil Moisture', color='g')
    ax.legend()
    ax.set_xlabel('Time')
    ax.set_ylabel('Values')
    canvas.draw()

def run_tkinter():
    global root, humidity_label, temperature_label, soil_moisture_label, canvas, ax

    root = tk.Tk()
    root.title("Smart Irrigation System")

    frame = ttk.Frame(root, padding="10")
    frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    humidity_label = ttk.Label(frame, text="Humidity: 0%")
    humidity_label.pack(pady=10)

    temperature_label = ttk.Label(frame, text="Temperature: 0 C")
    temperature_label.pack(pady=10)

    soil_moisture_label = ttk.Label(frame, text="Soil Moisture: 0")
    soil_moisture_label.pack(pady=10)

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title("Sensor Data Over Time")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    root.mainloop()

# Start Tkinter in a separate thread
tkinter_thread = threading.Thread(target=run_tkinter)
tkinter_thread.start()

# Run Flask server in the main thread
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
