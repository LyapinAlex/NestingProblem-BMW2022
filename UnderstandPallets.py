def understand_pallets(items):

    packing = []
    usedNumPallet = max([item.pallet_number for item in items])

    for i in range(usedNumPallet + 1):
        packing.append([])
        for item in items:
            if item.pallet_number == i:
                packing[i].append(item)

    return packing