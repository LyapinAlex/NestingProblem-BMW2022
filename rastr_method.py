import copy



def fit_item(pallet, item):

    for i in range(len(pallet[0])):
        for j in range(len(pallet)):
            exit = False
            # условия, что объект влезает
            if len(item) + i <= len(pallet) and len(item[0]) + j <= len(pallet[0]):
                # располагаем объект
                for p in range(len(item)):
                    for k in range(len(item[0])):
                        # решаем есть ли пересечение
                        if pallet[i+p][j+k] + item[p][k] == 2:
                            exit = True
                            break
                    if exit:
                        break
            else:
                exit = True
            # если пересечений нет и элемент влезает, то добавляем его
            if not exit:
                for p in range(len(item)):
                    for k in range(len(item[0])):
                        pallet[i+p][j+k] += item[p][k]
                break
        if not exit:
            break
    # print_matrix(pallet)
    # print('--------------')
    return pallet, exit

# def fit_list(matrix, items):
#     for item in items:
#         matrix, exit = fit_item(matrix, item)
#         # print_matrix(matrix)
#         # print('--------------')
#     return matrix


def fit_pallets(matrix, poligons):
    pallets = []
    pallets.append(copy.deepcopy(matrix))
    
    for poligon in poligons:

        i=0
        exit = True
        while exit and i<len(pallets):
            
        # for pallet in pallets:
            pallets[i], exit = fit_item(pallets[i], poligon)
            if exit and i==(len(pallets)-1):
                pallets.append(copy.deepcopy(matrix))
                #
            i+=1
    

    # print("finishAlg")
    return pallets

