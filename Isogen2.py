import dash
from dash import dcc
from dash import html
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def MeshGen():
    Xs = []
    Ys = []
    Zs = []
    i = -150000
    while i <= 150000:
        Xs.append(i)
        Ys.append(i)
        Zs.append(i)
        i = i + 20000
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
    return XYZs, X2s, Y2s, Z2s

def MeshFileReader(FileName):
    ErrorData = open(FileName)
    ErrorStats = ErrorData.readline().split()
    for i in ErrorStats:
        i = float(i)
    
    return ErrorStats

if __name__ == "__main__":
    print("Generating Mesh")
    XYZList, XList, YList, ZList = MeshGen()
    print(len(XList))
    print("reading values")
    MeshValues = MeshFileReader("MeshInterpolatedValues5")
    print(len(MeshValues))
    print("making figure")

    fig2 = go.Isosurface(
    x=XList,
    y=YList,
    z=ZList,
    value=MeshValues,
    opacity=0.15,
    colorscale = 'solar',
    isomin=25,
    isomax=25,
    surface_count=5, # number of isosurfaces, 2 by default: only min and max
    colorbar_nticks=5, # colorbar ticks correspond to isosurface values
    )
    Xg, Yg, Zg = np.mgrid[-6400:6400:100j, -6400:6400:100j, -6400:6400:100j]
    values = Xg * Xg + Yg * Yg + Zg * Zg
    
    fig1 = go.Isosurface(
    x=Xg.flatten(),
    y=Yg.flatten(),
    z=Zg.flatten(),
    value=values.flatten(),
    colorscale = [[0, 'rgb(0,0,0)'], [1, 'rgb(0,0,0)']],
    showscale = False,
    isomin=(6378**2),
    isomax=(6378**2),
    )
    

    fig3 = go.Figure(data = [fig1, fig2])

    fig3.show()
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig3)
])

app.run_server(debug=True, use_reloader=False)