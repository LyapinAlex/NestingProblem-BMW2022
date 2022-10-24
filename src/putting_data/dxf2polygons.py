import numpy as np


def dxf2polygons(path):
    file = open(path)
    polygonsList = []

    x = 0
    y = 0
    polygon = []
    beforeLine = ""

    for line in file:

        if line.strip() == "SEQEND" and len(polygon) != 0:
            polygon.pop()
            polygonsList.append(np.array(polygon))
            polygon = []

        if beforeLine.strip() == "10":
            x = float(line.strip())

        if beforeLine.strip() == "20":
            y = float(line.strip())
            polygon.append([x, y])

        beforeLine = line

    file.close()
    return np.array(polygonsList, dtype=object)

