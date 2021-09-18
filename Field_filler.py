import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from DataReader import read_file

def near(point, tree):
    dist, ind = tree.query(point, k = 1)

    return dist, ind

def expectedvals(point, pts, vals, tree):
    
    dist, ind = near(point, tree)
    conporp = float((vals[ind]))*(np.sqrt((float(pts[ind][0]))**2 + (float(pts[ind][1]))**2 + (float(pts[ind][2]))**2)**3)
    
    results = conporp/(np.sqrt((point[0])**2 + (point[1])**2 + (point[2])**2)**3)

    return results, dist

if __name__ == "__main__":
    input_filename = "ClusterDataOriginal.txt"
    lines_to_read = 10000000
    
    print("Reading data. . .")

    point_set, field_set = read_file(input_filename, lines_to_read)

    tree = cKDTree(point_set)

    YNop = "start"

    while YNop != "N":
        YNop = input("do you want to know the expected value of the field at a point (Y/N): ")
        if YNop == "N":
            break
        point = []
        x = input("What is your x coordinate: ")
        y = input("What is your y coordinate: ")
        z = input("What is your z coordinate: ")
        point.append(float(x))
        point.append(float(y))
        point.append(float(z))
        expect, dist = expectedvals(point, point_set, field_set, tree)
        print("The expected value of the field at your point is", expect)
        print("Your point is ", dist, " away from the nearest known point")




