

def pallet_quality(pallet, eps):
    record_height = 0
    for item in pallet:
        height = max([point[0]+item.lb_x*eps for point in item.points])
        if height > record_height:
            record_height = height
    return record_height
