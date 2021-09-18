import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.spatial import cKDTree
from scipy.interpolate import Rbf
from DataReader import read_file

def ErrorFileReader(FileName):
    ErrorData = open(FileName)
    ErrorStats = ErrorData.readline().split()
    for i in ErrorStats:
        i = float(i)
    
    return ErrorStats

def BestMethod(errorMatrix):
    minVec = []
    for i in errorMatrix[0]:
        for j in errorMatrix:
            temp = [errorMatrix[j][i], j]
            if j == 0:
                tempMax = temp
            if temp[0] < tempMax[0]:
                tempMax = temp
        minVec.append(tempMax)
        tempMax = 0
    return minVec

def MeshGen():
    Xs = []
    Ys = []
    Zs = []
    i = -142000
    while i <= 142000:
        Xs.append(i)
        Ys.append(i)
        Zs.append(i)
        i = i + 500
    XYZs = []
    for l in Xs:
        for j in Ys:
            for k in Zs:
                XYZs.append([l, j, k])
    X2s = []
    Y2s = []
    Z2s = []
    for pt in XYZs:
        X2s.append(pt[0])
        Y2s.append(pt[1])
        Z2s.append(pt[2])
    
    
        
def Interpolator(ptsKnown, valsKnown, tree, method, pt):
    if method == "NNerror":

    else:
        



if __name__ == "__main__":
    Comp = []
    FileNames = ("cubic", "gaussian", "inverse", "linear", "multiquadric", "quintic", "thin_plate", "NNerror")
    for name in FileNames:
        Temp = ErrorFileReader(name)
        Comp.append(Temp)
    
    
