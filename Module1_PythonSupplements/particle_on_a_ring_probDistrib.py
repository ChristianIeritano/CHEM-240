'''
2024-09-16
Author: CI
A python script that initalizes a GUI for plotting the real and imaginary parts of the wavefunctions defined by the rigid rotor approximation. 
This is meant to be a teaching tool for CHEM 240, which I taught in Fall 2024 at the University of Waterloo. 
To readers of this code: please use freely for the purpose of educating your students! 
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button, CheckButtons
from mpl_toolkits.mplot3d import Axes3D

# constnats
hbar = 1.0545718e-34  # Reduced Planck constant (J·s)

# Function to calculate reduced mass based on input masses
def reduced_mass(m1, m2):
    return (m1 * m2) / (m1 + m2)

# exponetial form of complex number is our rotation operator :)
def rotational_wavefunction_complex(n, theta):
    return np.exp(1j * n * theta)  # Returns real and complex parts of the wavefunction

# Function to handle button press and plot the real, imaginary parts, and optionally the probability distribution in 3D
def plot_wavefunction(event):
    try:
        n = int(textbox_n.text)
        m1 = float(textbox_m1.text)
        m2 = float(textbox_m2.text)
        r = float(textbox_r.text)  # Now, r is taken as input
        mu = reduced_mass(m1, m2)
        
        #define theta as 500 equidistant poins between 0 and 2pi
        theta = np.linspace(0, 2 * np.pi, 500)
        wavefunc = rotational_wavefunction_complex(n, theta)
        
        # Separate real and imaginary parts
        real_part = np.real(wavefunc)
        imag_part = np.imag(wavefunc)
        
        # Parametric circle in 3D (x = cos(theta), y = sin(theta), z = real/imag part of wavefunction)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        ax.clear()

        # plot a semi transparent circle to show the plane of rotation
        circle_theta = np.linspace(0, 2 * np.pi, 100)
        circle_x = r * np.cos(circle_theta)
        circle_y = r * np.sin(circle_theta)
        ax.plot_trisurf(circle_x, circle_y, np.zeros_like(circle_x), color='red', alpha=0.3)

        # plot real and imag parts in glorious 3D
        ax.plot(x, y, real_part, label=f'Real part (n={n})', lw=2, color='blue')
        ax.plot(x, y, imag_part, label=f'Imaginary part (n={n})', lw=2, color='green')

        # bit that plots prob distrib. if its clicked
        if checkbox_status[0]:
            probability_dist = (real_part + imag_part) * (real_part + imag_part.conjugate())
            ax.plot(x, y, probability_dist, label='Probability Distribution', lw=2, color='purple')
            #ax.plot_trisurf(x, y, probability_dist, color='purple', lw=2, alpha=0.8, label='Probability Distribution')

        ax.set_title('Rotational Wavefunction (Real, Imaginary Parts, and Probability Distribution)')
        ax.set_xlabel('X (A^2)')
        ax.set_ylabel('Y (A^2)')
        ax.set_zlabel(r'$\Psi_n(\theta)$')
        ax.grid(True)
        ax.legend()
        plt.draw()
    
    except ValueError:
        print('Invalid input! Please enter valid numbers for masses, bond length, and quantum number.')

def checkbox_func(label):
    checkbox_status[0] = not checkbox_status[0]
    plt.draw()

# Setup the plot and UI elements using Matplotlib
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.35)

# Pleaces to enter n, m1, m2, and r (yes, I nkow m1 and m2 aren'tr used, but this is a teaching tool for studnets :)
axbox_n = plt.axes([0.2, 0.35, 0.2, 0.05])
textbox_n = TextBox(axbox_n, 'Quantum number n:', initial="1")

axbox_m1 = plt.axes([0.2, 0.25, 0.2, 0.05])
textbox_m1 = TextBox(axbox_m1, 'Mass 1 (amu):', initial="1.0")

axbox_m2 = plt.axes([0.2, 0.15, 0.2, 0.05])
textbox_m2 = TextBox(axbox_m2, 'Mass 2 (amu):', initial="1.0")

axbox_r = plt.axes([0.2, 0.05, 0.2, 0.05])
textbox_r = TextBox(axbox_r, 'Bond length r (A**2):', initial="1.0")

# plot button
axbutton = plt.axes([0.5, 0.1, 0.1, 0.075])
button = Button(axbutton, 'Plot')

# button to plot prob distribution
axcheckbox = plt.axes([0.65, 0.1, 0.2, 0.1])
checkbox = CheckButtons(axcheckbox, ['Probability Distribution'], [False])
checkbox_status = [False]  # Track the state of the checkbox

button.on_clicked(plot_wavefunction)
checkbox.on_clicked(checkbox_func)

plt.show()
