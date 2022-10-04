from fileinput import filename
import numpy as np


class DxfReader:

    def __init__(self, path):
        self.path = path
        self.polygonsList = []

    def readDXF(self):
        self.file = open(self.path)

        x = 0
        y = 0
        polygon = []
        beforeLine = ""

        for line in self.file:

            if line.strip() == "POLYLINE" and len(polygon) != 0:
                polygon.pop()
                self.polygonsList.append(np.array(polygon))
                polygon = []

            if beforeLine.strip() == "10":
                x = float(line.strip())

            if beforeLine.strip() == "20":
                y = float(line.strip())
                polygon.append([x, y])

            beforeLine = line

        self.file.close()

        self.polygonsList = np.array(self.polygonsList, dtype=object)


if __name__ == "__main__":
    reader = DxfReader(
        r"C:\Users\1\Desktop\NestingProblem-BMW2022\src\input\NEST001-108.DXF")
    reader.readDXF()

    print(reader.polygonsList[1])
