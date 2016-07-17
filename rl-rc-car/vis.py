"""
Make a "matrix" plot of what the Robocar sees so we can see like it.
"""
import seaborn as sns
import matplotlib.pyplot as plt
import math

sns.set()


def visualize_polar(state):
    plt.clf()

    readings = state[0][:-1]

    r = []
    t = []
    for i, s in enumerate(readings):
        r.append(math.radians(i * 6))
        t.append(s)

    ax = plt.subplot(111, polar=True)

    ax.set_theta_zero_location('W')
    ax.set_ylim(bottom=0, top=105)

    plt.plot(r, t)
    plt.draw()
    plt.pause(0.1)


def visualize_sensors(state):
    # Clear.
    sns.plt.clf()

    # Reverse it.
    row = state[0][::-1]

    # Make a 2d list.
    cols = [row]

    # Plot it.
    sns.heatmap(data=cols, cmap="Blues_r", yticklabels=False)

    # Draw it.
    sns.plt.draw()

    # Add a pause because you're supposed to.
    sns.plt.pause(0.05)
