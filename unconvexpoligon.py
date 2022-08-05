import random
import numpy as np
import math
import matplotlib.pyplot as plt
import copy

def getVector():
    return [random.random(),random.random() ]


def norm(vec):
    return  math.sqrt(scalarProduc(vec, vec))

def scalarProduc(vecA, vecB):
    n = np.len(vecA)

    sp = 0
    for i in range(n):
        sp+= vecA[i]*vecB[i]

    return sp

# def vec
def vecDiff(vecA, vecB):
    return [vecA[0] - vecB[0], vecA[1] - vecB[1]]

def vecSum(vecA, vecB):
    return [vecA[0] + vecB[0], vecA[1] + vecB[1]]

def vecProduc(vecA, vecB):
    return vecA[0]*vecB[1] - vecA[1]*vecB[0]

def getOrderingTriangle(points):
    
    points = sorted(points, key=lambda point: point[0])
    firstPoint = sorted(points, key=lambda point: point[1] == sorted([point[1] for point in points])[0])[2]
    points.remove(firstPoint)
    
    points = sorted(points, key=lambda point: point[0])
    secondPoint = sorted(points, key=lambda point: point[1] == sorted([point[1] for point in points])[0])[1]
    points.remove(secondPoint)


    return [firstPoint, secondPoint, points[0]]



def getPolygon():
    
    # генерация произвольных точек
    points = [[random.random(),random.random() ] for __ in range(3)]
    
    # создание порядка на них
    points = getOrderingTriangle(points)

    return points
    
def checkCrossEdge(point, nextPoint, newEdge, lastPoints): 
    check = 0
    v_last = vecDiff(lastPoints, point)
    v_next = vecDiff(nextPoint, point) 
    v_new = vecDiff(newEdge, point )
    v = vecDiff(point, lastPoints )

    if vecProduc(v_last, v_new) * vecProduc(v_last, v_next) < 0:
        return check

    if vecProduc(vecDiff(lastPoints, nextPoint), vecDiff(newEdge, nextPoint )) * vecProduc(vecDiff(lastPoints, nextPoint), vecDiff(point, nextPoint) ) < 0:
        return check

    if vecProduc(v_last, v_new) * vecProduc(v_last, v_next) == 0:
        # print("точка на прямой")
        check = 1
        # кто то леит на прямой линии, пойми кто

    if vecProduc(v_last, v_new) * vecProduc(v_last, v_next) > 0:
        
        if vecProduc(v_next, v_new ) * vecProduc(v_next, v ) >= 0:
            # print("1")
            check = 1

    return check 


def showPolygon(points):
 
       

        for i in range(len(points)- 1):

            v_1 = np.array([points[i][0], points[i+1][0]])
            v_2 = np.array([points[i][1], points[i+1][1]])
            plt.plot(v_1, v_2, '-k')
        
        v_1 = np.array([points[len(points)- 1][0], points[0][0]])
        v_2 = np.array([points[len(points)- 1][1], points[0][1]])
        plt.plot(v_1, v_2, '-k')

        plt.show()


        return

def arpol(points, a, b, M = 4):
    
    pointsCopy = copy.deepcopy(points)
    # иттерация

    n = 3 # количество точек сейчас
    exitPolygon = 1
    while exitPolygon != 0:
        # print('1')
        pointsCopy = copy.deepcopy(points)
        exitPolygon = 0
        for k in  range(3, M):
            newPoint = [0, 0]
            exitPoint = 1
            while exitPoint!= 0:
                # print('2')
                exitPoint = 0
                phi = random.uniform(0, 2 * math.pi)
                r = random.uniform(a, b)
                newEdge = [r * math.cos(phi), r * math.sin(phi)]
                newPoint = vecSum(newEdge, pointsCopy[k - 1])
                for i in range(0, k - 2):
                    exitPoint+= checkCrossEdge(pointsCopy[i], pointsCopy[i + 1], vecSum(newEdge, pointsCopy[k - 1]), pointsCopy[k - 1])
                
            # проверка с началол
            pointsCopy.append(newPoint)
            # print(pointsCopy)
            # showPolygon(pointsCopy)


           
        for i in range(1, M - 2):
            # print(checkCrossEdge(pointsCopy[i], pointsCopy[i + 1], pointsCopy[0], pointsCopy[M - 1]))
            exitPolygon+= checkCrossEdge(pointsCopy[i], pointsCopy[i + 1], pointsCopy[0], pointsCopy[M - 1])
        
        

    return pointsCopy

def surfPolygon(points):

    # # вычисление размера массива
    # points = points.tolist()

    minX = sorted(points, key=lambda point: point[0])[0][0]
    minY = sorted(points, key=lambda point: point[1])[0][1]
    
    # print(minX)
    for point in points:
        point[0] = point[0] - minX
        point[1] = point[1] - minY
    
    # points = np.array(points)

    return points

# points = getPolygon()
# print(points)
# showPolygon(points)
# showPolygon(surfPolygon(arpol(getPolygon(), 1.0, 2.0, 5)))
# arpol(points, 0.0, 1.0)
# # print(points)
# arpol(points, 0.0, 1.0)
# # print(points)
# showPolygon(points)
# arpol(points, 0.0, 1.0)
# # print(points)
# showPolygon(points)
