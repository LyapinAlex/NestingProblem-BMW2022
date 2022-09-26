def understand_pallets(items):
    """Разделяет объекты в массивы по номеру палет"""
    packing = []
    itemsCom = []
    for item in items:
        if item.pallet_id != None:
            itemsCom.append(item)
    usedNumPallet = max([item.pallet_id for item in  itemsCom])

    for i in range(usedNumPallet  + 1):
        packing.append([])

    for i in range(usedNumPallet  + 1):
        for item in itemsCom:
            if item.pallet_id > len(packing):
                packing.append([])
            if item.pallet_id == i:
                packing[i].append(item)
    
    return packing