import random
import numpy as np
from scipy.interpolate import LinearNDInterpolator, Rbf
from run import read_data

random.seed(0)


if __name__ == "__main__":
    input_filename = "ClusterDataOriginal.txt"
    lines_to_read = 1000

    print("reading data...")
    pts, flxs = read_data(input_filename, lines_to_read)

    print("parsing data...")
    points = (
        [ float(p[0]) for p in pts ],
        [ float(p[1]) for p in pts ],
        [ float(p[2]) for p in pts ]
    )
    fluxes = [ float(f) for f in flxs ]

    print("creating interpolants...")
    linear_interpolator = LinearNDInterpolator(points, fluxes)
    rbfi_linear = Rbf(*points, fluxes, function="linear")
    rbfi_cubic = Rbf(*points, fluxes, function="cubic")
    rbfi_thin = Rbf(*points, fluxes, function="thin_plate")
    #rbfi_multiq = Rbf(*points, fluxes, function="multiquadric")
    #rbfi_inv = Rbf(*points, fluxes, function="inverse")
    #rbfi_gauss = Rbf(*points, fluxes, function="gaussian")
    #rbfi_quintic = Rbf(*points, fluxes, function="quintic")

    print("doing some interpolation...")
    point = [ (float(pts[0][i]) + float(pts[1][i])) / 2.0 for i in range(3) ]
    print(linear_interpolator(point))
    print("rbf linear:")
    print(rbfi_linear(*point))
    print("rbf cubic:")
    print(rbfi_cubic(*point))
    print("rbf thin:")
    print(rbfi_thin(*point))
    '''print("rbf multiquadric:")
    print(rbfi_multiq(*point))
    print("rbf inv:")
    print(rbfi_inv(*point))
    print("rbf gauss:")
    print(rbfi_gauss(*point))
    print("rbf quintic:")
    print(rbfi_quintic(*point))
    '''
