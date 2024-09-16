'''
2024-09-9
Author: CI
A python script that initalizes a GUI for simulating expected binomial distributions given a number of flips performed across N trials (Total flips = Flips * trials).

If the simulate button is pressent, the distribution of outcomes of Total flips = Flips * trials will be overlaid with the expected distribution. 
Users can tune the fairness of the flipping simulation with the "Sim Fairness" input. Likewise, the expected binomial distribution that shows in the background can be tuned to whatever fairness you want via the "base fairness" input (betwene 0 and 1).
Finally, a printout of the p-value of the simulation vs. the p-value that the coin is done, and a CRUDE COMPARISON is performed where if the p_sim < "confidence interval" (0 to 1), then we can say that the coin is unfair within the CI%.

To readers of this code: please use freely for the purpose of educating your students! 
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from scipy.stats import binom

# plot binom distib function
def plot_binomial_distribution(n_flips, fairness):
    ax.clear()

    # range of possible outcomes (number of heads)
    x = np.arange(0, n_flips + 1)

    # binomial distribution for the given fairness
    probabilities = binom.pmf(x, n_flips, fairness) * n_flips
    
    # Plotting the theoretical histogram of probabilities
    ax.bar(x, probabilities, color='skyblue', alpha=0.7, label=f"PMF (Fairness = {fairness})")
    
    # adjust the x-axis dynamically to +/- 10% of the number of flips
    lower_bound = binom.ppf(0.0005, n_flips, fairness)
    upper_bound = binom.ppf(0.9995, n_flips, fairness)
    margin = 0.1 * (upper_bound - lower_bound)
    ax.set_xlim([max(0, lower_bound - margin), min(n_flips, upper_bound + margin)])
    
    # stuff to describe the plot
    ax.set_title(f"Probability Distribution of Heads after {n_flips} Flips\n(Fairness = {fairness})")
    ax.set_xlabel("Number of Heads")
    ax.set_ylabel("(Expected) # occurances")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), shadow=True, ncol=2)
    ax.grid(True)
    
    plt.draw()

# simulate coin flips and calculate the probability that the coin is unfair using p-hacking
def simulate_coin_flip(n_flips, n_trials, simulate_fairness, plot_fairness, confidence_level):
    ax.clear()

    nheads = np.random.binomial(n_flips, simulate_fairness, n_trials)
    
    #do some math to figure out the total proportion of heads rolled (h)
    total_heads = np.sum(nheads)
    h = np.mean(nheads) / (n_flips) 

    # Adjust the x-axis dynamically to +/- 10% of the number of flips
    lower_bound = binom.ppf(0.0005, n_flips, simulate_fairness)
    upper_bound = binom.ppf(0.9995, n_flips, simulate_fairness)
    margin = 0.1 * (upper_bound - lower_bound)
    ax.set_xlim([max(0, lower_bound - margin), np.ceil(upper_bound + margin)])

    # recalc fair binomial distribution
    x = np.arange(0, n_flips + 1)
    expected_probabilities = binom.pmf(x, n_flips, plot_fairness)

    # calc the frequency of each outcome (number of heads) in the simulation & plot
    simulated_counts = np.bincount(nheads, minlength=n_flips + 1)
    ax.bar(x, simulated_counts, alpha=0.5, color='red', label="Simulated Flips (Number of Heads)") 
        
    # plot fair distrib
    ax.bar(x, (expected_probabilities * n_trials), color='skyblue', alpha=0.7, label=f"PMF (Base fairness)") 
  
    ax.set_title(f"Simulated Results and Fair Distribution\nObserved Proportion of Heads: {h:.4f}")
    ax.set_xlabel("Number of Heads")
    ax.set_ylabel("(Expected) # occurances")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), shadow=True, ncol=2)
    ax.grid(True)

    plt.draw()
    
    return  #return total number of heads - needed for some p hacking

# stuff for update the text printout within the GUI interface - thanks ChatGPT :)
def update(val=None):
    try:
        n_flips = int(text_flips.text)
        fairness = float(text_fairness.text)
        if not (0 <= fairness <= 1):
            unfair_probability_text.set_text("Fairness must be between 0 and 1.")
            return
        plot_binomial_distribution(n_flips, fairness)
        unfair_probability_text.set_text("Awaiting simulation...")
    except ValueError as e:
        unfair_probability_text.set_text(f"Invalid input. Please enter valid numbers: {e}")

# same for when the sim button is pressed. Math is me, integration is thanks to chatgpt
def simulate(event):
    try:
        n_flips = int(text_flips.text)
        n_trials = int(text_trials.text)
        plot_fairness = float(text_fairness.text)
        simulate_fairness = float(text_simulate_fairness.text)
        confidence_level = float(text_confidence.text)
        
        if not (0 <= simulate_fairness <= 1):
            unfair_probability_text.set_text("Simulate fairness must be between 0 and 1.")
            return
        
        if not (0 < confidence_level < 1):
            unfair_probability_text.set_text("Confidence level must be between 0 and 1.")
            return
        
        # Simulate and calculate unfair probability
        nheads = simulate_coin_flip(n_flips, n_trials, simulate_fairness, plot_fairness, confidence_level) #simulate the coin flip, update the plot, and return number of heads flipped

        # Calculating the p-value for two tails considering both fewer and greater outcomes than observed heads
        p_value_lower = binom.cdf(nheads, n_flips * n_trials, 0.5)
        p_value_upper = binom.sf(nheads, n_flips * n_trials, 0.5)

        # Two-tailed test p-value
        p_value = 2 * min(p_value_lower, p_value_upper)
        p_value = min(p_value, 1)  # Ensure p-value does not exceed 1     

        if p_value < (1 - confidence_level):
            unfair_probability_text.set_text(f'UNFAIR COIN! {nheads} heads after {n_flips} flips {n_trials} times. p= {np.round(p_value, 2)} < {np.round(1 - confidence_level, 2)} (unfair within {np.round(confidence_level*100, 0)}% CI).')
        else:
            unfair_probability_text.set_text(f'FAIR COIN! {nheads} heads after {n_flips} flips {n_trials} times. p= {np.round(p_value, 2)} > {np.round(1 - confidence_level, 2)} (fair within {np.round(confidence_level*100, 0)}% CI).')
    except ValueError as e:
        unfair_probability_text.set_text(f"Invalid input. Please enter valid numbers")
        print(e)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.55)

# Set up text boxes for number of flips, fairness for the plot, simulate fairness, and confidence level
ax_flips_text = plt.axes([0.2, 0.3, 0.15, 0.05])
ax_fairness_text = plt.axes([0.6, 0.3, 0.15, 0.05])

text_flips = TextBox(ax_flips_text, 'Flips:', initial="10")

text_fairness = TextBox(ax_fairness_text, 'Base Fairness:', initial="0.5")

ax_separator_text = plt.axes([0.1, 0.2, 0.8, 0.03])
ax_separator_text.axis('off')  # Hide the axis
ax_separator_text.text(0.5, 0.5, "Simulate Fairness and Confidence Interval", fontsize=12, ha='center')

ax_simulate_fairness_text = plt.axes([0.2, 0.15, 0.15, 0.05])
ax_confidence_text = plt.axes([0.6, 0.15, 0.15, 0.05])
ax_trials_text = plt.axes([0.2, 0.1, 0.15, 0.05])
text_simulate_fairness = TextBox(ax_simulate_fairness_text, 'Sim Fairness:', initial="0.5")
text_trials = TextBox(ax_trials_text, 'Trials:', initial="10")
text_confidence = TextBox(ax_confidence_text, 'Confidence Level:', initial="0.95")

# sim button
simulate_ax = plt.axes([0.8, 0.15, 0.1, 0.05])
simulate_button = Button(simulate_ax, 'Simulate', color='lightblue', hovercolor='skyblue')

# print statement window
ax_output_text = plt.axes([0.1, 0.01, 0.8, 0.1])  # Adjust the size of the output text box
ax_output_text.axis('off')  # Remove the weird y-axis
unfair_probability_text = ax_output_text.text(0, 0.5, "Awaiting simulation...", fontsize=10, transform=ax_output_text.transAxes)

# stuff to do the things when sim is clicked
text_flips.on_submit(update)
text_trials.on_submit(update)
text_fairness.on_submit(update)
simulate_button.on_clicked(simulate)

# always show fair binom distib on startup
plot_binomial_distribution(10, 0.5)

plt.show()
