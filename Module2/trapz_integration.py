import numpy as np
import matplotlib.pyplot as plt

'''
Author: CI
A simple python code that plots a function defined by the input to f(x) and the trapezoids used to approximate its integral between the bounds a < x < b. 
Users can define the number of trapezoids used in the numerical integration. 
Output is a plot showing the function, trapezoids, and the approximate area under the curve between the bounds [a,b].
'''

# Define the function to integrate
def f(x):
    return np.sin(x)  

a = 0  # Lower bound
b = np.pi  # Upper bound
n = 100  # Number of trapezoids

#Actual integration - input the functional form of the true integration
def int_f(x):
    return -1. * np.cos(x) 

true_int = np.round((int_f(b) - int_f(a)), 6)

###
#   This is the brains of the code. If you're a student and playing around with things, only edit stuff below this point if you know what you are doing!!!
###

# Generate x values and calculate the width of each trapezoid
x = np.linspace(a, b, n + 1)
y = f(x)
h = (b - a) / n

# trapezoid rule area calcualtion (I could use np.trapz, but because I have to define a specific number of trapezoids for plotting, might as well do it this way)
area = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])

# Plot fxn
x_fine = np.linspace(a, b, 500)
y_fine = f(x_fine)
plt.plot(x_fine, y_fine, 'k-', label='f(x)')  

# Plot trapezoids
for i in range(n):
    x_trap = [x[i], x[i], x[i+1], x[i+1]]
    y_trap = [0, y[i], y[i+1], 0]
    plt.fill(x_trap, y_trap, 'green', alpha=0.5, edgecolor='black') 

# text stating approximate area
plt.text(a + 0.01 * (b - a), max(y) * 0.95, f'Approx. area = {area:.8f}', 
         fontsize=12, color='blue', ha='left', bbox=dict(facecolor='white', alpha=0.5))

plt.text(a + 0.01 * (b - a), max(y) * 0.85, f'Approx. area = {true_int:.8f}', 
         fontsize=12, color='blue', ha='left', bbox=dict(facecolor='white', alpha=0.5))

# make snd show plot
plt.title(f'Trapezoidal Method for Integration. True int: {true_int}')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.show()
