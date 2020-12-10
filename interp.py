import random
import numpy as np
from scipy.interpolate import LinearNDInterpolator, Rbf
from run import read_data, write_points_to_file

random.seed(0)

def split_data(x, y, prob, sample_size):
    """Splits the data into two groups: a training group and a testing group.
    Elements from x and y will be put into the testing group with probability
    prob. The returned value will be of the form: train_x, train_y, test_x,
    test_y.

    Args:
        x (list): The x values of the data
        y (list): The y values of the data
        prob (double): The probability of a (x,y) pair to be added to the test set
        sample_size (int): The total number of datapoints to sample
    """
    test_x = []
    test_y = []
    train_x = []
    train_y = []

    for i in range(sample_size):
        r = random.random()
        if r < prob:
            test_x.append(x[i])
            test_y.append(y[i])
        else:
            train_x.append(x[i])
            train_y.append(y[i])

    return train_x, train_y, test_x, test_y

def print_interpolation_method_stats(interp, x, y):
    y_hat = interp(*x)
    error = y_hat - y
    max_error = abs(max(error.min(), error.max(), key=abs))

    print("absolute error (2-norm): ", np.linalg.norm(error))
    print("relative error (2-norm): ", np.linalg.norm(error) / np.linalg.norm(y))
    print("average error: ", np.linalg.norm(error, 1) / len(y))
    print("max error: ", max_error)
    print("-------------------------------------------------------------------")

def print_list_stats(l):
    print("Maximum: ", np.max(l))
    print("Minimum: ", np.min(l))
    print("Average: ", np.average(l))
    print("Standard deviation: ", np.std(l))
    print("Count: ", len(l))

if __name__ == "__main__":
    input_filename = "ClusterDataOriginal.txt"
    lines_to_read = 10000000

    print("-------------------------------------------------------------------")
    print("reading data...")
    pts, flxs = read_data(input_filename, lines_to_read)
    flxs = [ float(f) for f in flxs ]
    print("Flux stats:")
    print_list_stats(flxs)

    print("-------------------------------------------------------------------")
    print("shuffling data...")
    temp = list(zip(pts, flxs))
    #random.shuffle(temp)
    pts, flxs = zip(*temp)

    print("-------------------------------------------------------------------")
    print("Splitting data...")
    training_points, training_fluxes, test_points, test_fluxes = split_data(pts, flxs, 0.1, 10000) # DO NOT EXCEED 10000 (on my dinky laptop...)

    #write_points_to_file("training.vtk", training_points, training_fluxes)
    #write_points_to_file("testing.vtk", test_points, test_fluxes)

    print("Training flux stats:")
    print_list_stats(training_fluxes)
    print("Testing flux stats:")
    print_list_stats(test_fluxes)

    training_points = np.transpose(training_points)
    test_points = np.transpose(test_points)

    print("-------------------------------------------------------------------")
    print("Interpolating...")
    methods = ["linear", "cubic", "thin_plate"]
    for method in methods:
        rbf_interpolator = Rbf(*training_points, training_fluxes, function=method)
        print("Method: ", method)
        print_interpolation_method_stats(rbf_interpolator, test_points, test_fluxes)
