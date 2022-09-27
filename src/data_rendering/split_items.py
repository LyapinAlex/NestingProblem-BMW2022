def split_items(packaging):
    """Разделяет объекты в массивы по номеру палет"""

    split_pal = [[] for i in range(packaging.num_pallets)]
    for item in packaging.items: 
        if item.pallet_id != None:
            split_pal[item.pallet_id].append(item)
    
    return split_pal
