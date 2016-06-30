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


def plot_file(filename, data_type='loss'):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Turn our column into an array.
        y = []
        for row in reader:
            if data_type == 'loss':
                y.append(float(row[0]))
            else:
                y.append(float(row[1]))

    # Running tests will be empty.
    if len(y) == 0:
        return

    # Get the moving average so the graph isn't so crazy.
    if data_type == 'loss':
        window = 100
    else:
        window = 10
    y_av = movingaverage(y, window)

    # Use our moving average to get some metrics.
    arr = np.array(y_av)
    if data_type == 'loss':
        print("%f\t%f\n" % (arr.min(), arr.mean()))
    else:
        print("%f\t%f\n" % (arr.max(), arr.mean()))

    # Plot it.
    plt.clf()  # Clear.
    plt.title(data_type)
    # The -50 removes an artificial drop at the end caused by the moving
    # average.
    if data_type == 'loss':
        plt.plot(y_av[:-50])
        plt.ylabel('Smoothed Loss')
        # plt.ylim(0, 5000)
        # plt.xlim(0, 1000)
    else:
        plt.plot(y_av[:-5])
        plt.ylabel('Smoothed Distance')
        # plt.ylim(0, 4000)
        # plt.xlim(0, 4000)
    plt.show()


if __name__ == "__main__":
    plot_file('results/loss-log.csv', 'loss')
    plot_file('results/distances.csv', 'distance')
