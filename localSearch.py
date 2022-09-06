import rastr_method
import copy


def swap(list, pos1, pos2):
     
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


#  алгоритм локального пояска
def locSearch(matrix, poligons):

    # смотрит сколько элементов
    n = len( poligons)
    
    
    objVal = len(rastr_method.fit_pallets(matrix,  copy.deepcopy(poligons)))

    betterNeighboor = (0,0)
    for i in range(n):
        for j in range(i + 1, n, 1):
            val = len(rastr_method.fit_pallets(matrix, swap( copy.deepcopy(poligons), i, j)))
      
            if val < objVal:
                
                objVal = val
                betterNeighboor = (i,j)

    
    if betterNeighboor[1] != 0:
        poligons = swap( poligons, betterNeighboor[0], betterNeighboor[1])

    if betterNeighboor[1] != 0:
        locSearch(matrix, poligons)
    
    return poligons
    

    
