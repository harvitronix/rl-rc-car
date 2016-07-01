"""
Plot results.
"""
import csv
import matplotlib.pyplot as plt
import numpy as np


def movingaverage(y, window_size):
    """
    Moving average function from:
    http://stackoverflow.com/questions/11352047/finding-moving-average-from-data-points-in-python
    """
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(y, window, 'same')


def plot_file(filename):
    y = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Turn our column into an array.
        for row in reader:
            y.append(float(row[0]))

    # Running tests will be empty.
    if len(y) == 0:
        return

    # Get the moving average so the graph isn't so crazy.
    y_av = movingaverage(y, 100)

    # Use our moving average to get some metrics.
    arr = np.array(y_av)
    print("%f\t%f\n" % (arr.min(), arr.mean()))

    # Plot it.
    plt.clf()  # Clear.
    # The -50 removes an artificial drop at the end caused by the moving
    # average.
    plt.plot(y_av[:-50])
    plt.ylabel('Smoothed Loss')
    plt.show()


if __name__ == "__main__":
    plot_file('results/loss-log.csv')
