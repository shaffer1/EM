import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from scipy.interpolate import Rbf
from DataReader import read_file

if __name__ == "__main__":
    input_filename = "ClusterDataOriginal.txt"
    lines_to_read = 10000000
    
    pts, vals = read_file(input_filename, lines_to_read)
    dist_max = 0
    for i in pts:
        temp_dist = np.sqrt((float(i[0]))**2 + (float(i[1]))**2 + (float(i[2]))**2)
        if temp_dist > dist_max:
            dist_max = temp_dist

    print(dist_max)

