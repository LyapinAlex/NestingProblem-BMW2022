import copy

from class_item import Item


def create_items():
    # poligon1 = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    # poligon2 = [[1, 1], [1, 0]]
    # poligon3 = [[1, 1, 1], [0, 1, 0]]
    #
    # points_1 = [[0, 3], [2, 0], [3, 1], [2, 1], [1, 4]]
    # points_2 = [[0, 0], [1, 0], [1, 8], [0, 8]]
    # points_3 = [[0, 3], [2, 0], [2, 1], [3, 2], [1, 4]]

    sq_points = [[0, 0], [0, 2], [2, 2], [2, 0]]
    sq_matrix = [[1, 1], [1, 1]]
    point_23 = [[0, 0], [0, 3], [2, 3], [2, 0]]
    matrix_23 = [[1, 1, 1], [1, 1, 1]]
    point_big = [[0, 0], [0, 3], [3, 3], [3, 6], [9, 6], [9, 0]]
    matrix_big = [[1, 1, 1, 0, 0, 0], [1, 1, 1, 0, 0, 0], [1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]
    point_ugol = [[4, 0], [4, 4], [0, 4], [0, 5], [5, 5], [5, 0]]
    matrix_ugol = [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [1, 1, 1, 1, 1]]
    point_ugol_niz = [[3, 0], [3, 4], [0, 4], [0, 5], [4, 5], [4, 0]]
    matrix_ugol_niz = [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [1, 1, 1, 1, 1]]
    point_gor = [[0, 0], [0, 7], [1, 7], [1, 3], [3, 3], [3, 0]]
    matrix_gor = [[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0]]

    poligons = [copy.deepcopy(sq_points), copy.deepcopy(sq_points), copy.deepcopy(sq_points), copy.deepcopy(sq_points),
                copy.deepcopy(sq_points), copy.deepcopy(sq_points), copy.deepcopy(sq_points),
                copy.deepcopy(sq_points), copy.deepcopy(sq_points), copy.deepcopy(sq_points), copy.deepcopy(sq_points),
                copy.deepcopy(sq_points), copy.deepcopy(sq_points), copy.deepcopy(sq_points),
                copy.deepcopy(point_23), copy.deepcopy(point_23), copy.deepcopy(point_23),
                copy.deepcopy(point_23), copy.deepcopy(point_23), copy.deepcopy(point_23),
                copy.deepcopy(point_big),
                copy.deepcopy(point_big),
                copy.deepcopy(point_ugol),
                copy.deepcopy(point_ugol),
                copy.deepcopy(point_ugol_niz),
                copy.deepcopy(point_ugol_niz),
                copy.deepcopy(point_gor),
                copy.deepcopy(point_gor)]

    # poligons = [copy.deepcopy(points_2),copy.deepcopy(points_2)]
    items = [Item(i, poligons[i]) for i in range(len(poligons))]

    for i in range(14):
        items[i].matrix = copy.deepcopy(sq_matrix)

    items[14].matrix = copy.deepcopy(matrix_23)
    items[15].matrix = copy.deepcopy(matrix_23)
    items[16].matrix = copy.deepcopy(matrix_23)
    items[17].matrix = copy.deepcopy(matrix_23)
    items[18].matrix = copy.deepcopy(matrix_23)
    items[19].matrix = copy.deepcopy(matrix_23)
    items[20].matrix = copy.deepcopy(matrix_big)
    items[21].matrix = copy.deepcopy(matrix_big)
    items[22].matrix = copy.deepcopy(matrix_ugol)
    items[23].matrix = copy.deepcopy(matrix_ugol)
    items[24].matrix = copy.deepcopy(matrix_ugol_niz)
    items[25].matrix = copy.deepcopy(matrix_ugol_niz)
    items[26].matrix = copy.deepcopy(matrix_gor)
    items[27].matrix = copy.deepcopy(matrix_gor)

    return items
