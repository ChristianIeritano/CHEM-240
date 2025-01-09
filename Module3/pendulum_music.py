import tkinter as tk
from tkinter import simpledialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pygame
import time

# Initialize pygame for sound playback
pygame.mixer.init()

# Function to generate a sound for each pendulum
def play_sound(index):
    sound = pygame.mixer.Sound(f'sound{index}.wav')  # Predefined sounds for each pendulum
    sound.play()

# Pendulum class to model the motion of each pendulum
class Pendulum:
    def __init__(self, length, mass, phase, sound_index):
        self.length = length
        self.mass = mass
        self.phase = phase
        self.sound_index = sound_index
        self.theta = phase
        self.omega = 0  # Initial angular velocity
        self.g = 9.81  # Gravity constant

    def update(self, dt):
        # Simple pendulum equation: d2theta/dt2 = -(g/L) * sin(theta)
        alpha = -(self.g / self.length) * np.sin(self.theta)  # Angular acceleration
        self.omega += alpha * dt  # Update angular velocity
        self.theta += self.omega * dt  # Update angle

        # If the pendulum crosses the center (theta == 0), play sound
        if abs(self.theta) < 0.05 and abs(self.omega) > 0:  # Threshold for crossing
            play_sound(self.sound_index)

    def get_position(self):
        # Calculate x, y positions of the pendulum
        x = self.length * np.sin(self.theta)
        y = -self.length * np.cos(self.theta)
        return x, y

# GUI Class to define pendulum parameters
class PendulumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pendulum Music App")

        # Initialize parameters
        self.num_pendulums = 0
        self.pendulums = []

        # GUI Elements
        self.num_label = tk.Label(root, text="Number of Pendulums:")
        self.num_label.pack()
        self.num_entry = tk.Entry(root)
        self.num_entry.pack()

        self.mass_phase_label = tk.Label(root, text="Enter mass, phase (degrees) for each pendulum:")
        self.mass_phase_label.pack()

        self.mass_phase_text = tk.Text(root, height=10, width=40)
        self.mass_phase_text.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_simulation)
        self.start_button.pack()

    def start_simulation(self):
        try:
            self.num_pendulums = int(self.num_entry.get())
            if self.num_pendulums <= 0:
                raise ValueError("Number of pendulums must be greater than 0.")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        # Parse mass and phase for each pendulum
        input_text = self.mass_phase_text.get("1.0", tk.END).strip().split("\n")
        if len(input_text) != self.num_pendulums:
            messagebox.showerror("Input Error", "Please provide mass and phase for each pendulum.")
            return

        self.pendulums = []
        for idx, line in enumerate(input_text):
            try:
                mass, phase = map(float, line.split(","))
                pendulum = Pendulum(length=1, mass=mass, phase=np.radians(phase), sound_index=idx+1)
                self.pendulums.append(pendulum)
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid input for pendulum {idx+1}.")
                return

        self.animate_pendulums()

    def animate_pendulums(self):
        fig, ax = plt.subplots()
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 0.5)
        lines = [ax.plot([], [], lw=2)[0] for _ in range(self.num_pendulums)]
        bob = [ax.plot([], [], 'o', markersize=10)[0] for _ in range(self.num_pendulums)]

        def init():
            for line in lines:
                line.set_data([], [])
            for b in bob:
                b.set_data([], [])
            return lines + bob

        def update(frame):
            dt = 0.01  # Time step for updating pendulums
            for idx, pendulum in enumerate(self.pendulums):
                pendulum.update(dt)
                x, y = pendulum.get_position()
                lines[idx].set_data([0, x], [0, y])  # Line from origin to bob
                bob[idx].set_data([x], [y])          # Bob as a single point
            return lines + bob


        ani = FuncAnimation(fig, update, frames=500, init_func=init, blit=True, interval=50)
        plt.show()

# Main Tkinter application
root = tk.Tk()
app = PendulumApp(root)
root.mainloop()
