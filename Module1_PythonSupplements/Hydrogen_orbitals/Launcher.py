'''
Author: CI only for the main controller. 
The remaining python bits were made verabatim from the genius that is  liam-ilan:
https://github.com/liam-ilan/electron-orbitals
Credit for all script except for main.py go to him. If you adapt this code for your teaching, please cite him accordingly. Also, please use his website:
https://liam-ilan.github.io/electron-orbitals
'''

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from hydrogen import cartesian_prob, cartesian_prob_real

# initialize main window
root = tk.Tk()
root.title("Orbital Plotter")

fig = plt.figure(figsize=(8,6)) #you may need to fiddle with this size depending on the resolution of your screen!
canvas = FigureCanvasTkAgg(fig, master=root)

def plot_orbital():
    try:
        n = int(n_entry.get())
        l = int(l_entry.get())
        m = int(m_entry.get())
        plot_type = plot_type_var.get()

        # Validate quantum numbers
        if n < 1 or l < 0 or l >= n or abs(m) > l:
            raise ValueError("Invalid quantum numbers!")

        fig.clear()

        ax = fig.add_subplot(111, projection='3d')

        # define plot type
        if plot_type == "Real":
            render_3d_to_ax(ax, n, l, m, 'real')
        elif plot_type == "Complex":
            render_3d_to_ax(ax, n, l, m, 'complex')

        canvas.draw()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# plotting function
def render_3d_to_ax(ax, n, l, m, mode):
    
    # some resolution definitions
    render_radius = 8 * n
    s = 30  
    step = render_radius / s

    # lists to store ddata
    x_data, y_data, z_data, p_data, alpha_data = [], [], [], [], []

    for x in range(-s, s):
        for y in range(-s, s):
            for z in range(-s, s):
                if mode == 'real':
                    p = cartesian_prob_real(n, l, m, x * step, y * step, z * step)
                elif mode == 'complex':
                    p = cartesian_prob(n, l, m, x * step, y * step, z * step)

                if p > 0.00001:  # Threshold to plot only significant probabilities - needs to be lower for high value of n
                    x_data.append(x * step)
                    y_data.append(y * step)
                    z_data.append(z * step)
                    p_data.append(p)

                    # Normalize p for transparency: we want low probabiltiy points to drop off FAST
                    alpha = 1.00 - 0.9 * (1 - (p / max(p_data))**6)
                    alpha_data.append(alpha)
    
    # Check if we have data to plot
    if len(p_data) == 0:
        messagebox.showerror("Error", "No significant data to plot. Adjust quantum numbers.")
        return
    
    ax.scatter(x_data, y_data, z_data, c=p_data, cmap='viridis', marker='o', alpha=alpha_data)
    ax.set_xlabel('X axis (a₀)')
    ax.set_ylabel('Y axis (a₀)')
    ax.set_zlabel('Z axis (a₀)')
    ax.set_title(f'3D {mode.capitalize()} Orbital (n={n}, l={l}, m={m})')

# input fields
ttk.Label(root, text="n (Principal quantum number):").grid(row=0, column=0, padx=10, pady=5)
n_entry = ttk.Entry(root)
n_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="l (Azimuthal quantum number):").grid(row=1, column=0, padx=10, pady=5)
l_entry = ttk.Entry(root)
l_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(root, text="m (Magnetic quantum number):").grid(row=2, column=0, padx=10, pady=5)
m_entry = ttk.Entry(root)
m_entry.grid(row=2, column=1, padx=10, pady=5)

# plot tpye selector
plot_type_var = tk.StringVar()
plot_type_dropdown = ttk.OptionMenu(root, plot_type_var, "Real", "Real", "Complex")
ttk.Label(root, text="Select Plot Type:").grid(row=3, column=0, padx=10, pady=5)
plot_type_dropdown.grid(row=3, column=1, padx=10, pady=5)

plot_button = ttk.Button(root, text="Plot", command=plot_orbital)
plot_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

canvas.get_tk_widget().grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# start gui
root.mainloop()
