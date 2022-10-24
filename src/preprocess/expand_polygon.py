import math
import numpy as np
import matplotlib.pyplot as plt


list_points = np.array([[592.205, 683.901], [593.992, 680.914], [594.958, 680.656], [596.495, 679.457], [596.705, 677.52], [577.463, 644.192], [575.68, 643.405], [573.874, 644.137], [573.167, 644.845], [569.687, 644.898], [538.79, 627.06], [537.097, 624.02], [537.356, 623.054], [537.087, 621.123], [535.514, 619.973], [497.03, 619.973], [495.457, 621.123], [495.188, 623.053], [495.447, 624.02], [493.754, 627.06], [462.857, 644.898], [459.377, 644.844], [458.67, 644.138], [456.864, 643.405], [455.081, 644.192], [435.839, 677.52], [436.049, 679.457], [437.586, 680.655], [438.553, 680.915], [440.339, 683.901], 
[440.339, 719.577], [438.553, 722.564], [437.586, 722.824], [436.049, 724.021], [435.839, 725.959], [455.081, 759.286], [456.864, 760.073], [458.67, 759.341], [459.377, 758.634], [462.857, 758.58], [493.754, 776.418], [495.447, 779.459], [495.188, 780.426], [495.457, 782.355], [497.03, 783.506], [535.514, 783.506], [537.087, 782.355], [537.356, 780.425], [537.097, 779.459], [538.79, 776.418], [569.687, 758.58], [573.167, 758.634], [573.874, 759.342], [575.68, 760.073], [577.463, 759.286], [596.705, 725.959], [596.495, 724.021], [594.958, 722.823], [593.992, 722.565], [592.205, 719.577], [592.205, 683.9]])

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

def get_vec_sub(v_1, v_2):

    return [v_1[0] - v_2[0], v_1[1] - v_2[1]]

def show2Polygons(points_1, points_2):
 
       
    for i in range(len(points_1)- 1):

        v_1 = np.array([points_1[i][0], points_1[i+1][0]])
        v_2 = np.array([points_1[i][1], points_1[i+1][1]])
        plt.plot(v_1, v_2, '-k')

    for i in range(len(points_2)- 1):
        v_1 = np.array([points_2[i][0], points_2[i+1][0]])
        v_2 = np.array([points_2[i][1], points_2[i+1][1]])
        plt.plot(v_1, v_2, '-r')
    
    v_1 = np.array([points_1[len(points_1)- 1][0], points_1[0][0]])
    v_2 = np.array([points_1[len(points_1)- 1][1], points_1[0][1]])
    plt.plot(v_1, v_2, '-k')
    v_1 = np.array([points_2[len(points_2)- 1][0], points_2[0][0]])
    v_2 = np.array([points_2[len(points_2)- 1][1], points_2[0][1]])
    plt.plot(v_1, v_2, '-r')



    plt.show()


    return


def get_orient(points):

    v_1 = get_vec_sub(points[1], points[0])
    v_2 = get_vec_sub(points[2], points[1])

    if v_1[0]*v_2[1] - v_1[1] * v_2[0] > 0:
        return True
    else:

        return False


def get_neighboring_points(i, list):

    long = len(list)

    i = i % long
    
    if i == 0:
        return (list[-1], list[0], list[1])
    elif i == long - 1 :
        return (list[-2], list[-1], list[0])
    else:
        return (list[i - 1], list[i], list[i + 1])


def pereform_points(points, eps):



    # убираем дубликаты
    list_points = points.tolist()
    
    list_points_without_doupl = []

    for el in list_points:
        if el not in list_points_without_doupl:
            list_points_without_doupl.append(el)
    
    # убираем точки на прямых

    for i in range(len(list_points_without_doupl) - 2):
        
        v_1 = get_vec_sub(list_points_without_doupl[i + 1], list_points_without_doupl[i])
        v_2 = get_vec_sub(list_points_without_doupl[i + 2], list_points_without_doupl[i])
        
        if v_1[0]*v_2[1] - v_1[1] * v_2[0] == 0:
            list_points_without_doupl.pop(i + 1)

    v_1 = get_vec_sub(list_points_without_doupl[0], list_points_without_doupl[-2])
    v_2 = get_vec_sub(list_points_without_doupl[-1], list_points_without_doupl[-2])
    
    if v_1[0]*v_2[1] - v_1[1] * v_2[0] == 0:
        list_points_without_doupl.pop(-1)

    v_1 = get_vec_sub(list_points_without_doupl[1], list_points_without_doupl[-1])
    v_2 = get_vec_sub(list_points_without_doupl[0], list_points_without_doupl[-1])
    
    if v_1[0]*v_2[1] - v_1[1] * v_2[0] == 0:
        list_points_without_doupl.pop(0)
    minpos = np.argmin(list_points, axis=0)[0]

    polygon_orient= get_orient(get_neighboring_points(minpos, list_points))
    
    for i in range(len(list_points_without_doupl)):
        points = get_neighboring_points(minpos + i,  list_points_without_doupl)
        convex = convex_angle(points, polygon_orient)
        if not convex:
            v_1 = get_vec_sub(points[0], points[1])
            v_2 = get_vec_sub(points[2], points[1])
            
            if get_nor_vec(v_1) < eps or get_nor_vec(v_2) < eps:
                
                long = len(list_points_without_doupl)

                list_points_without_doupl.pop( (minpos + i) % long)
                



    
    return np.array(list_points_without_doupl)

def convex_angle(points, orient = True):

    v_1 = get_vec_sub(points[1], points[0])
    v_2 = get_vec_sub(points[2], points[1])

    if v_1[0]*v_2[1] - v_1[1] * v_2[0] > 0:
        return orient
    else:

        return not orient


def get_nor_vec(vec):
    return math.sqrt(vec[0]**2 + vec[1]**2)


def creat_new_point(points, eps, convex_angle):
  
    v_1 = points[0] - points[1]
    v_2 = points[2] - points[1]
    v_1 = v_1 / get_nor_vec(v_1)
    v_2 = v_2 / get_nor_vec(v_2)


    cos = (v_1[0]*v_2[0] + v_1[1]*v_2[1]) / (get_nor_vec(v_1) * get_nor_vec(v_2))
    sin = math.sqrt( 1 - cos**2)

    angle = 0
    if convex_angle:
        angle = -1
    else:
        angle = 1

    v = (v_1 + v_2) * ( angle * eps / sin)

    new_point = v + points[1]

    return new_point

def expand_polygon(list_points, eps):

    new_polygon = []

    minpos = np.argmin(list_points, axis=0)[0]

    list_points = pereform_points(list_points, eps)
    
    minpos = np.argmin(list_points, axis=0)[0]
    polygon_orient= get_orient(get_neighboring_points(minpos, list_points))

    for i in range(len(list_points)):
        points = get_neighboring_points(i + minpos, list_points)
        convex = convex_angle(points, polygon_orient)
        new_point = creat_new_point(points, eps, convex)
        new_polygon.append(new_point)

    return np.array(new_polygon)

