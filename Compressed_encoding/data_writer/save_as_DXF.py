import ezdxf

def save_pallet_as_DXF(path, pallet) -> None:
    doc = ezdxf.new()
    msp = doc.modelspace()
    for position in pallet.plased_items_positions:
        points = position.polygon_on_position.points_to_list()
        msp.add_polyline2d(points, close=True)
    
    points = pallet.original_pallet.points_to_list()
    msp.add_polyline2d(points, close=True)

    doc.saveas(path[:-4] + '-' + str(pallet.id) + '.dxf')

def save_as_DXF(path, packing) -> None:
    for pallet in packing.pallets:
        save_pallet_as_DXF(path, pallet)
