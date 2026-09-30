import tkinter as tk
from tkinter import messagebox
import serial
import serial.tools.list_ports
import threading
import time

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MCBControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MCB Testing Control Center with Live Current Graph")
        self.root.geometry("600x650")
        self.root.configure(bg="#1e1e2e")

        self.ser = None
        self.is_running = True

        self.time_data = []
        self.current_data = []

        # --- UI Header ---
        header = tk.Label(root, text="SYSTEM CONTROLLER & CURRENT GRAPH", font=("Segoe UI", 11, "bold"), fg="#cdd6f4", bg="#181825")
        header.pack(fill="x", ipady=10)

        # --- Stepper Motor Controls ---
        stepper_frame = tk.LabelFrame(root, text=" Stepper Motor (1.3 Turns) ", font=("Segoe UI", 9, "bold"), bg="#1e1e2e", fg="#a6adc8")
        stepper_frame.pack(fill="x", padx=15, pady=10)

        self.btn_cw = tk.Button(stepper_frame, text="ISOLATE(1.3)", font=("Segoe UI", 9, "bold"), bg="#89b4fa", fg="#11111b", bd=0, height=2, command=lambda: self.send_command('CW\n'))
        self.btn_cw.pack(side="left", expand=True, fill="x", padx=10, pady=8)

        self.btn_ccw = tk.Button(stepper_frame, text="CONTACT (1.3)", font=("Segoe UI", 9, "bold"), bg="#b4befe", fg="#11111b", bd=0, height=2, command=lambda: self.send_command('CCW\n'))
        self.btn_ccw.pack(side="right", expand=True, fill="x", padx=10, pady=8)

        # --- Embedded Plot Frame ---
        graph_frame = tk.LabelFrame(root, text=" 5-Second Time vs Current Graph ", font=("Segoe UI", 9, "bold"), bg="#1e1e2e", fg="#a6adc8")
        graph_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.fig = Figure(figsize=(5, 3.2), dpi=100)
        self.fig.patch.set_facecolor('#1e1e2e')
        self.ax = self.fig.add_subplot(111)
        self.configure_plot()

        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        # --- Status Footer ---
        self.status_label = tk.Label(root, text="Status: Connecting...", font=("Segoe UI", 9), fg="#a6adc8", bg="#181825")
        self.status_label.pack(fill="x", ipady=6, side="bottom")

        self.connect_serial()

        self.thread = threading.Thread(target=self.read_serial_data, daemon=True)
        self.thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_plot(self):
        self.ax.set_facecolor('#181825')
        self.ax.set_title("MCB Trip Event: Current over 5 Second", color='#cdd6f4', fontsize=10)
        self.ax.set_xlabel("Time (ms)", color='#a6adc8', fontsize=8)
        self.ax.set_ylabel("Current (A)", color='#a6adc8', fontsize=8)
        self.ax.tick_params(colors='#a6adc8', labelsize=8)
        self.ax.grid(True, color='#313244', linestyle='--', linewidth=0.5)
        self.ax.set_xlim(0, 5000)
        self.ax.set_ylim(0, 100)

    def connect_serial(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if any(x in p.description for x in ["USB", "UART", "CH340", "FTDI"]):
                try:
                    self.ser = serial.Serial(p.device, 9600, timeout=1)
                    time.sleep(2)
                    self.status_label.config(text=f"Connected on {p.device}")
                    return
                except Exception:
                    pass
        self.status_label.config(text="Status: Disconnected (Check COM Port)", fg="#f38ba8")

    def send_command(self, cmd):
        if self.ser and self.ser.is_open:
            self.ser.write(cmd.encode())
        else:
            messagebox.showerror("Serial Error", "Device not connected via USB-to-TTL!")

    def update_graph(self):
        self.ax.clear()
        self.configure_plot()
        if self.time_data and self.current_data:
            self.ax.plot(self.time_data, self.current_data, color='#f9e2af', linewidth=2, marker='o', markersize=3)
            max_curr = max(self.current_data)
            self.ax.set_ylim(0, max(100, max_curr * 1.2))
        self.canvas.draw()

    def read_serial_data(self):
        while self.is_running:
            if self.ser and self.ser.is_open:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line.startswith("EVENT:"):
                        self.time_data.clear()
                        self.current_data.clear()
                        self.status_label.config(text="Sampling 5-second current waveform...", fg="#fab387")
                    elif line.startswith("DATA:"):
                        parts = line.replace("DATA:", "").split(",")
                        t_val = float(parts[0])
                        i_val = float(parts[1])
                        self.time_data.append(t_val)
                        self.current_data.append(i_val)
                    elif line == "GRAPH_COMPLETE":
                        self.root.after(0, self.update_graph)
                        self.status_label.config(text="Graph updated successfully!", fg="#a6e3a1")
                    elif line.startswith("STATUS:"):
                        self.status_label.config(text=line, fg="#89b4fa")
                except Exception:
                    pass
            time.sleep(0.01)

    def on_close(self):
        self.is_running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MCBControlApp(root)
    root.mainloop()
