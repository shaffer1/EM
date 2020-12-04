import random
import numpy as np
from scipy.interpolate import LinearNDInterpolator, Rbf
from run import read_data

random.seed(0)
interpolation_methods = [
    "linear",
    "cubic",
    "thin_plate",
    "multiquadric",
    "inverse",
    "gaussian",
    "quintic"
]

def print_interpolation_method_stats(interp, x, y):
    y_hat = interp(*x)
    error = y_hat - y
    max_error = abs(max(error.min(), error.max(), key=abs))

    print("absolute error (2-norm): ", np.linalg.norm(error))
    print("relative error (2-norm): ", np.linalg.norm(error) / np.linalg.norm(y))
    print("max error: ", max_error)
    print("-------------------------------------------------------------------")

if __name__ == "__main__":
    input_filename = "ClusterDataOriginal.txt"
    lines_to_read = 10000 # DO NOT EXCEED 10000 (on my dinky laptop...)

    print("reading data...")
    pts, flxs = read_data(input_filename, lines_to_read)

    print("parsing data...")
    points = (
        [ float(p[0]) for p in pts ],
        [ float(p[1]) for p in pts ],
        [ float(p[2]) for p in pts ]
    )
    fluxes = [ float(f) for f in flxs ]

    print("randomizing data...")
    chance = 0.1
    training_points = ([], [], [])
    training_fluxes = []
    test_points = ([], [], [])
    test_fluxes = []

    total_training_data = 0
    total_test_data = 0
    for i in range(len(fluxes)):
        r = random.random()
        if r < chance:
            total_test_data += 1
            test_points[0].append(points[0][i])
            test_points[1].append(points[1][i])
            test_points[2].append(points[2][i])
            test_fluxes.append(fluxes[i])
        else:
            total_training_data += 1
            training_points[0].append(points[0][i])
            training_points[1].append(points[1][i])
            training_points[2].append(points[2][i])
            training_fluxes.append(fluxes[i])
    print("Total train data: ", total_training_data)
    print("Total test data: ", total_test_data)

    print("creating interpolants...")
    linear_interpolator = LinearNDInterpolator(training_points, training_fluxes)
    rbfi_linear = Rbf(*training_points, training_fluxes, function="linear")
    rbfi_cubic = Rbf(*training_points, training_fluxes, function="cubic")
    rbfi_thin = Rbf(*training_points, training_fluxes, function="thin_plate")

    print("interpolating...")
    print("Linear")
    print_interpolation_method_stats(linear_interpolator, test_points, test_fluxes)
    print("RBF Linear")
    print_interpolation_method_stats(rbfi_linear, test_points, test_fluxes)
    print("RBF Cubic")
    print_interpolation_method_stats(rbfi_cubic, test_points, test_fluxes)
    print("RBF Thin Plate")
    print_interpolation_method_stats(rbfi_thin, test_points, test_fluxes)
