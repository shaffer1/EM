def read_data(file, line_count):
    data_file = open(file)
    headers = data_file.readline().split()

    x_idx = headers.index("X")
    y_idx = headers.index("Y")
    z_idx = headers.index("Z")
    mag_flux_idx = headers.index("B_tot")

    points = []
    fluxes = []

    total_lines_gotten = 0
    while total_lines_gotten < line_count:
        line = data_file.readline().split()
        if "nan" in line:
            continue
        if len(line) == 0:
            print("No more lines to read. Got " + str(total_lines_gotten) + " lines.")
            break

        point = (line[x_idx], line[y_idx], line[z_idx])
        points.append(point)
        fluxes.append(line[mag_flux_idx])
        total_lines_gotten += 1

    data_file.close()

    return points, fluxes

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
        file.write("1 " + str(i) + "\n")

def write_vtk_cell_types(file, count):
    file.write("CELL_TYPES " + str(count) + "\n")
    for _ in range(count):
        file.write("1\n")

def write_vtk_point_data(file, data):
    file.write("POINT_DATA " + str(len(data)) + "\n")
    file.write("SCALARS field_strength float 1\n")
    file.write("LOOKUP_TABLE default\n")
    for d in data:
        file.write(str(d) + " ")
    file.write("\n")

def write_points_to_file(filename, points, fluxes):
    output = open(filename, "w+")
    write_vtk_header(output)
    write_vtk_points(output, points)
    write_vtk_cells(output, len(points))
    write_vtk_cell_types(output, len(points))
    write_vtk_point_data(output, fluxes)
    output.close()

if __name__ == "__main__":
    input_filename = "ClusterDataOriginal.txt"
    output_filename = "output.vtk"
    lines_to_read = 1000000

    print("Reading data...")
    points, fluxes = read_data(input_filename, lines_to_read)

    print("Writing vtk output...")
    write_points_to_file(output_filename, points, fluxes)
    '''output = open(output_filename, "w+")
    write_vtk_header(output)
    write_vtk_points(output, points)
    write_vtk_cells(output, len(points))
    write_vtk_cell_types(output, len(points))
    write_vtk_point_data(output, fluxes)
    output.close()'''

    print("Done.")
