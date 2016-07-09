"""
Make a "matrix" plot of what the Robocar sees so we can see like it.
"""
import seaborn as sns

sns.set()


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
