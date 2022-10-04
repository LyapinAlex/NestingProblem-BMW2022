def fit_item(pallet, item_matrix, i, j):
    """Располагает предмет на палете, без проверки на пересечение"""
    for p in range(item_matrix.shape[0]):
        k = 0
        while k < item_matrix.shape[1]:
            if  item_matrix[p][k] > 0:
                pallet[i+p][j+k] += item_matrix[p][k]
                k += 1
            else:
                k -= item_matrix[p][k]
    return None