import ezdxf


def items2DXF(items, pallet_width, pallet_height):
    doc = ezdxf.new()
    msp = doc.modelspace()
    for item in items:
        if (item.points[0][0] != item.points[-1][0]
                or item.points[0][1] != item.points[-1][1]):
            item.points = item.points.tolist()
            item.points.append(item.points[0])
        msp.add_polyline2d(item.points)
        
    msp.add_polyline2d([(0, 0), (0, pallet_height),
                        (pallet_width, pallet_height), (pallet_width, 0),
                        (0, 0)])
    doc.saveas('src\output\pallet' + str(items[0].pallet_id) + '.DXF')
