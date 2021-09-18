def read_file(filename, linetot):
    data = open(filename)
    headers = data.readline().split()
    Bindex = headers.index("B_tot")
    xindex = headers.index("X")
    yindex = headers.index("Y")
    zindex = headers.index("Z")
    coordinates = []
    Barray = []

    i = 0
    while i < linetot:
        templn = data.readline().split()
        if "nan" in templn:
            continue
        if len(templn) == 0:
            print("Finished reading data")
            break
        pointtemp = (templn[xindex], templn[yindex], templn[zindex])
        coordinates.append(pointtemp)
        Barray.append(templn[Bindex])
        i += 1
    data.close()
    return coordinates, Barray
