import math

if __name__=='__main__':
    from check_item import check_item
    from fit_item import fit_item
else:
    from .check_item import check_item
    from .fit_item import fit_item

def fit_item_with_route(pallet, item):
    """Выбирает лучший поворот предмета и располагает его на палете, с проверкой на пересечение"""
    list_matrix = item.list_matrix 
    N_x = pallet.shape[0] + 1
    N_y = pallet.shape[1] + 1
    rout = 0
    placed_item = False
    for r in range(4):  
        sol = check_item(pallet,  list_matrix[r])
        if sol[0] and ((sol[1] + len(list_matrix[r]) < N_x) or (sol[1] + len(list_matrix[r]) < N_x  and sol[2] < N_y)):
            item.lb_x = sol[1]
            item.lb_y = sol[2]
            item.rotation = r * math.pi / 2

            N_x = sol[1]  + len(list_matrix[r])
            N_y = sol[2]  
            rout = r
            placed_item = True

    if placed_item:
        fit_item(pallet, list_matrix[rout], item.lb_x, item.lb_y)
  
    return not placed_item