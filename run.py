
def write_vtk_header(file):
    file.write("# vtk DataFile Version 3.0\n")
    file.write("Output\n")
    file.write("ASCII\n\n")
    file.write("DATASET UNSTRUCTURED_GRID\n")

def write_vtk_points(file, points):
    file.write("POINTS " + str(len(points)) + " float\n")
    for point in points:
        file.write(point[0])
        file.write(" ")
        file.write(point[1])
        file.write(" ")
        file.write(point[2])
        file.write("\n")

def write_vtk_cells(file, count):
    file.write("CELLS " + str(count) + " " + str(2*count) + "\n")
    for i in range(count):
        output.write("1 " + str(i) + "\n")

def write_vtk_cell_types(file, count):
    file.write("CELL_TYPES " + str(count) + "\n")
    for _ in range(count):
        output.write("1\n")

def write_vtk_point_data(file, data):
    file.write("POINT_DATA " + str(len(data)) + "\n")
    file.write("SCALARS field_strength float 1\n")
    file.write("LOOKUP_TABLE default\n")
    for d in data:
        file.write(d + " ")
    file.write("\n")



if __name__ == "__main__":
    input_filename = "ClusterDataOriginal.txt"
    output_filename = "output.vtk"
    lines_to_read = 1000000

    data_file = open(input_filename)
    headers = data_file.readline().split()

    x_idx = headers.index("X")
    y_idx = headers.index("Y")
    z_idx = headers.index("Z")
    mag_flux_idx = headers.index("B_tot")

    points = []
    fluxes = []

    print("Reading data...")

    for _ in range(lines_to_read):
        line = data_file.readline().split()
        if "nan" in line:
            continue
        if len(line) == 0:
            break

        point = (line[x_idx], line[y_idx], line[z_idx])
        points.append(point)
        fluxes.append(line[mag_flux_idx])
    data_file.close()

    print("Writing vtk output...")

    output = open(output_filename, "w+")
    write_vtk_header(output)
    write_vtk_points(output, points)
    write_vtk_cells(output, len(points))
    write_vtk_cell_types(output, len(points))
    write_vtk_point_data(output, fluxes)
    output.close()

    print("Done.")
