"""
Author: TheJoe570
Version: 1.0.0.0
Description: This script creates a system information overlay display showing CPU usage, memory usage, and GPU usage. Designed for Nvidia GPU. I could create more functions for other cards if requested.
Date: February 28, 2024
Contact: TheJoe570@gmail.com
License: This script is provided under the MIT License.

 MIT License

Copyright (c) 2024 TheJoe570

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

**Conditions**:
If you modify the source code, you must include a statement in the modified
source code indicating that the original author of the software is TheJoe570.

"""

import tkinter as tk
import psutil
import threading
import time
import subprocess

# Function to update system information
def update_system_info():
    while True:
        # CPU usage
        cpu_percent = psutil.cpu_percent()
        cpu_label.config(text=f"CPU Usage: {cpu_percent}%")

        # Memory usage
        memory_percent = psutil.virtual_memory().percent
        memory_label.config(text=f"Memory Usage: {memory_percent}%")

        # GPU usage
        try:
            cmd = "nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits"
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                gpu_utilization = result.stdout.strip()
                gpu_label.config(text=f"GPU Usage: {gpu_utilization}%")
            else:
                raise subprocess.CalledProcessError(result.returncode, cmd)
        except Exception as e:
            gpu_label.config(text="GPU Usage: N/A")

        time.sleep(1)  # Update every second

# Function to update transparency based on window size
def update_transparency(event):
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    transparency_level = 0.7  # Adjust the transparency level as needed (0.0 - 1.0)
    root.attributes("-alpha", transparency_level)

# Create Tkinter window
root = tk.Tk()
root.title("System Usage")

# Set background color to black
root.configure(bg="black")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Window size and position
window_width = 300
window_height = 65
x_position = screen_width - window_width
y_position = screen_height - window_height

# Adjust y_position to place the window above the taskbar
y_position -= 80
x_position -= 10

# Set the window position and size
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Bind function to update transparency on window resize
root.bind("<Configure>", update_transparency)

# Labels for system information with white text color
cpu_label = tk.Label(root, font=("Arial", 12), fg="white", bg="black", anchor="w", padx=10)
cpu_label.pack(fill="x")

memory_label = tk.Label(root, font=("Arial", 12), fg="white", bg="black", anchor="w", padx=10)
memory_label.pack(fill="x")

gpu_label = tk.Label(root, font=("Arial", 12), fg="white", bg="black", anchor="w", padx=10)
gpu_label.pack(fill="x")

# Start thread to update system information
update_thread = threading.Thread(target=update_system_info)
update_thread.daemon = True  # Daemonize thread to stop it when the main thread exits
update_thread.start()

# Run the Tkinter event loop
root.mainloop()
