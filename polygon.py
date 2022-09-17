import numpy as np
import random as rd
import matplotlib.pyplot as plt
import math

from sqlalchemy import true


def norm(vec):
    return math.sqrt(scalarProduc(vec, vec))


def scalarProduc(vecA, vecB):
    n = np.len(vecA)

    sp = 0
    for i in range(n):
        sp += vecA[i]*vecB[i]

    return sp


def vecProduc(vecA, vecB):
    return vecA[0]*vecB[1] - vecA[1]*vecB[0]


def checkCross(vecA, vecB):
    check = 0
    rez = vecProduc(vecA, vecB)

    if rez > 0:
        check = 1

    if rez < 0:
        check = -1

    return check

# def definitionOfOrderTriongle(points):
#     indFirst = -1
#     xFirst = 10
#     for i in range(3):
#         if points[i,0] < xFirst:
#             indFirst = i
#             xFirst = points[i,0]

#     indSecond = -1
#     ySecond = 10
#     for i in range(3):
#         if points[i,1] < ySecond and i != indFirst :
#             indSecond = i
#             ySecond = points[i,1]

#     listInd = [0, 1, 2]
#     listInd.remove(indFirst)
#     listInd.remove(indSecond)


#     return [indFirst, indSecond, listInd[0]]


def definitionOfOrderTriongle(points):

    points = points.tolist()
    points = sorted(points, key=lambda point: point[0])
    firstPoint = sorted(points, key=lambda point: point[1] == sorted(
        [point[1] for point in points])[0])[2]
    points.remove(firstPoint)

    points = sorted(points, key=lambda point: point[0])
    secondPoint = sorted(points, key=lambda point: point[1] == sorted(
        [point[1] for point in points])[0])[1]
    points.remove(secondPoint)

    return np.array([firstPoint, secondPoint, points[0]])


def getConvexPolygon(n, w, l):
    # print(n, w, l)
    p = Polygon()
    x = rd.normalvariate(3*w / 4, w / 4)
    y = rd.normalvariate(3*l / 4, l / 4)
    p.extension(x, y)
    # print(x,y, 'pol')
    p.setPowerOfPolygon(n)

    return p


class Polygon():

    def __init__(self):
        self.powerOfPolygon = 3  # количество вершин

        # Сначало создаем треугольник и определяем порядок точек, как против часовой
        rng = np.random.default_rng()
        points = rng.random((3, 2))  # создвем три точки в 2-D

        self.points = definitionOfOrderTriongle(points)
        self.edge = np.array([[0, 1], [1, 2], [2, 0]])
        self.order = np.array([0, 1, 2])
        self.convex = True

        return

    def addVertex(self):

        # выбираем ребо с второго по предпоследнее
        m = rd.randint(1, self.powerOfPolygon - 2)
        #  иницализируем вектора
        vecLast = self.points[self.edge[m][0]] - \
            self.points[self.edge[m - 1][0]]
        vecNext = self.points[self.edge[m][1]] - \
            self.points[self.edge[m + 1][1]]
        # Вектор выбраного ребра, направлен в от меньшого значения к большему
        vecEdge = self.points[self.edge[m][1]] - self.points[self.edge[m][0]]

        check = checkCross(vecLast, vecNext)

        x = rd.random()
        y = rd.random()

        newPoint = np.array([0.0, 0.0])
        # вектора при соседнях ребрах коллинераны
        if check == 0:
            newPoint += x * vecLast + y * vecEdge

        # вектора не пересикаются
        if check == 1:
            newPoint += x * vecLast + y * vecNext

        # вектора пересикаются
        if check == -1:
            vecHelp = self.points[self.edge[m + 1][1]] - \
                self.points[self.edge[m - 1][0]]
            t = vecProduc(vecHelp, vecNext) / vecProduc(vecLast, vecNext) - 1
            newVecLast = t * vecLast

            if x + y >= 1:

                if x > y:
                    x -= 0.5
                else:
                    y -= 0.5

            newPoint += x * newVecLast + y * vecEdge

        newPoint += self.points[self.edge[m][0]]
        self.addPoint(newPoint, m)

        return

    def addPoint(self, newPoint, m):
        self.order = np.append(self.order, self.powerOfPolygon)
        self.edge = np.delete(self.edge, -1, 0)
        self.edge = np.append(
            self.edge, [[self.powerOfPolygon - 1, self.powerOfPolygon]], axis=0)
        self.edge = np.append(self.edge, [[self.powerOfPolygon, 0]], axis=0)
        self.points = np.insert(self.points, m + 1, newPoint, axis=0)
        self.powerOfPolygon += 1
        return

    def setPowerOfPolygon(self, n):
        if n < self.powerOfPolygon:
            print("АХТУНГ!!! Ты  заставляешь многограник уменьшить количество вершин!!!")

        for __ in range(n - self.powerOfPolygon):
            self.addVertex()

        return

    def showPolygon(self):

        for edge in self.edge:
            v_1 = np.array([self.points[edge[0]][0], self.points[edge[1]][0]])
            v_2 = np.array([self.points[edge[0]][1], self.points[edge[1]][1]])
            plt.plot(v_1, v_2, '-k')

        for point in self.points:

            plt.plot(point[0], point[1], 'ro')

        plt.show()

        return

    def extension(self, x, y):

        for i in range(self.powerOfPolygon):
            self.points[i, 0] = self.points[i, 0]*x
            self.points[i, 1] = self.points[i, 1]*y

        return

    def surfPolygon(self):

        # вычисление размера массива
        self.points = self.points.tolist()

        minX = sorted(self.points, key=lambda point: point[0])[0][0]
        minY = sorted(self.points, key=lambda point: point[1])[0][1]

        # print(minX)
        for point in self.points:
            point[0] = point[0] - minX
            point[1] = point[1] - minY

        self.points = np.array(self.points)

        return self.points
    # def coordinate


if __name__ == "__main__":
    # print("Ты не должен запускать этот файл на прямую!!! Пользуйся интерфейсом generate.py!!!")0
    p = Polygon()
    p.setPowerOfPolygon(4)
    p.showPolygon()
    p.surfPolygon()
    p.showPolygon()
