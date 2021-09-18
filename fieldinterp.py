import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from DataReader import read_file

random.seed(0)

def expectedvals(testinds, pts, vals, ind):
    
    conporp = float((vals[ind]))*(np.sqrt((float(pts[ind][0]))**2 + (float(pts[ind][1]))**2 + (float(pts[ind][2]))**2)**3)
    
    results = []

    i = 0
    while i < len(testinds):
        func = conporp/(np.sqrt((float(pts[testinds[i]][0]))**2 + (float(pts[testinds[i]][1]))**2 + (float(pts[testinds[i]][2]))**2)**3)
        results.append(func)
        i += 1

    return results

def knowns(testinds, vals):
    results = []

    i = 0
    while i < len(testinds):
        func = float(vals[testinds[i]])
        results.append(func)
        i += 1

    return results

def comp(exact, expected, dist):
    
    i = 0

    absolute_error_avg = 0
    relative_error_avg = 0
    max_absolute_error = 0
    max_relative_error = 0
    distace_avg = 0
    distance_max = 0

    while i < len(exact):
        absolute_error = abs(expected[i] - exact[i])
        relative_error = (abs((expected[i] - exact[i])/exact[i]))*100
        absolute_error_avg += absolute_error
        relative_error_avg += relative_error
        distace_avg += dist[i]
        if max_absolute_error < absolute_error:
            max_absolute_error = absolute_error
        if max_relative_error < relative_error:
            max_relative_error = relative_error    
        if distance_max < dist[i]:
            distance_max = dist[i]
        i += 1

    absolute_error_avg = absolute_error_avg/len(exact)
    relative_error_avg = relative_error_avg/len(exact)
    distace_avg = distace_avg/len(exact)
    print("The average absolute error is ", absolute_error_avg)
    print("The average relative error is ", relative_error_avg, "percent")
    print("The maximum absolute error is ", max_absolute_error)
    print("The maximum relative error is ", max_relative_error, "percent")
    print("The average distance betweem points is ", distace_avg)
    print("The maximum distance between points is ", distance_max)

def comp2(exact, expected):
    
    i = 0

    absolute_error_avg = 0
    relative_error_avg = 0
    max_absolute_error = 0
    max_relative_error = 0

    while i < len(exact):
        absolute_error = abs(expected[i] - exact[i])
        relative_error = (abs((expected[i] - exact[i])/exact[i]))*100
        absolute_error_avg += absolute_error
        relative_error_avg += relative_error
        
        if max_absolute_error < absolute_error:
            max_absolute_error = absolute_error
        if max_relative_error < relative_error:
            max_relative_error = relative_error    

        i += 1

    absolute_error_avg = absolute_error_avg/len(exact)
    relative_error_avg = relative_error_avg/len(exact)
    print("The average absolute error is ", absolute_error_avg)
    print("The average relative error is ", relative_error_avg, "percent")
    print("The maximum absolute error is ", max_absolute_error)
    print("The maximum relative error is ", max_relative_error)

def field_func(pts, vals):
    rand1 = random.randrange(0, len(vals))
    interp_func = vals[rand1]

    return interp_func, rand1

def approx_func(pts, vals, tree, radius):
    base_index = random.randrange(0, len(vals))
    indicies = tree.query_ball_point(pts[base_index], radius)
    
    basept = [float(pts[base_index][0]), float(pts[base_index][1]), float(pts[base_index][2])]

    distances = []
    weights = []
    consts = []

    i = 0
    while i < len(indicies):
        tempdist = np.sqrt((float(pts[indicies[i]][0]) - basept[0])**2 + (float(pts[indicies[i]][1]) - basept[1])**2 + (float(pts[indicies[i]][2]) - basept[2])**2)
        distances.append(tempdist)
        weights.append(1/((tempdist+1)**2))
        tempconst = float((vals[indicies[i]]))*(np.sqrt((float(pts[indicies[i]][0]))**2 + (float(pts[indicies[i]][1]))**2 + (float(pts[indicies[i]][2]))**2)**3)
        tempconst = tempconst*weights[i - 1]
        consts.append(tempconst)
        i += 1

    avg_const = 0
    i = 0

    while i < len(consts):
        avg_const += consts[i]
        i += 1
    
    i = 0
    weightsum = 0
    while i < len(consts):
        weightsum += weights[i]
        i += 1

    avg_const = avg_const/weightsum
    
    expected = []
    i = 0
    while i < len(indicies):
        func = avg_const/(np.sqrt((float(pts[indicies[i]][0]))**2 + (float(pts[indicies[i]][1]))**2 + (float(pts[indicies[i]][2]))**2)**3)
        expected.append(func)
        i += 1

    exact = []
    i = 0
    while i < len(indicies):
        func = float(vals[indicies[i]])
        exact.append(func)
        i += 1

    return expected, exact

def NNinterp_allpts(tree, pts, vals):
    absolute_error_avg = 0
    relative_error_avg = 0
    max_absolute_error = 0
    max_relative_error = 0
    distace_avg = 0
    distance_max = 0
    
    distance_arr = []
    relative_arr = []
    absolute_arr = []

    i = 0
    
    while i < len(pts):
        distance, nearest = tree.query(pts[i], k = 2)
        conporp = float((vals[i]))*(np.sqrt((float(pts[i][0]))**2 + (float(pts[i][1]))**2 + (float(pts[i][2]))**2)**3)
        expected = conporp/(np.sqrt((float(pts[nearest[1]][0]))**2 + (float(pts[nearest[1]][1]))**2 + (float(pts[nearest[1]][2]))**2)**3)
        exact = float(vals[nearest[1]])
        absolute_error = abs(expected - exact)
        relative_error = (abs((expected - exact)/exact))*100
        absolute_error_avg += absolute_error
        relative_error_avg += relative_error
        distace_avg += distance[1]
        if max_absolute_error < absolute_error:
            max_absolute_error = absolute_error
        if max_relative_error < relative_error:
            max_relative_error = relative_error    
        if distance_max < distance[1]:
            distance_max = distance[1]
        distance_arr.append(distance[1])
        relative_arr.append(relative_error)
        absolute_arr.append(absolute_error)

        i += 1

    absolute_error_avg = absolute_error_avg/len(pts)
    relative_error_avg = relative_error_avg/len(pts)
    distace_avg = distace_avg/len(pts)

    print("The average absolute error is ", absolute_error_avg)
    print("The average relative error is ", relative_error_avg, "percent")
    print("The maximum absolute error is ", max_absolute_error)
    print("The maximum relative error is ", max_relative_error, " percent")
    print("The average distance betweem points is ", distace_avg)
    print("The maximum distance between points is ", distance_max)

    fig = plt.figure()
    
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.scatter(distance_arr, relative_arr)
    ax2.scatter(distance_arr, absolute_arr)
    ax1.set_title('Relative')
    ax1.set_ylabel('Relative Error')
    ax1.set_xlabel('Distance')

    ax2.set_title('Absolute')
    ax2.set_ylabel('Absolute Error')
    ax2.set_xlabel('Distance')
    plt.show()
        
if __name__ == "__main__":
    input_filename = "ClusterDataOriginal.txt"
    lines_to_read = 10000000
    i = 0
    test_number = 10
    test_point_number = 10
    
    print("Reading data. . .")

    point_set, field_set = read_file(input_filename, lines_to_read)

    print("Here is the interpolation method:")

    tree = cKDTree(point_set)

    while i < test_number:
        
        fieldval, idx = field_func(point_set, field_set)
        distances, indicies = tree.query(point_set[idx], k = test_point_number)
    
        expect = expectedvals(indicies, point_set, field_set, idx)
    
        known = knowns(indicies, field_set)
        print("------------------------------------------------------------------------------------------------")
        print("This is the itteration of point ", i + 1, " of the test, testing the accuracy for the ", test_point_number, "nearest points")
        comp(known, expect, distances)
        i += 1
        test_point_number += 1
    
    print("------------------------------------------------------------------------------------------------")
    print("Here is a method via approximation:")
    i = 0
    while i < test_number:
        expect, known = approx_func(point_set, field_set, tree, 2000)
        print("------------------------------------------------------------------------------------------------")
        print("This is the itteration of point set ", i + 1)
        comp2(known, expect)
        i += 1

    print("------------------------------------------------------------------------------------------------")
    print("Here are interpolation results for modified nearest point interpolation scheme over all of the points:")
    NNinterp_allpts(tree, point_set, field_set)
    
 