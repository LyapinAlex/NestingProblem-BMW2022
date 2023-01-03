from matplotlib import pyplot as plt
from .primitives import image_size, focusing_on_subject, draw_polygon, draw_compressed_encoding


def save_pallet_as_PNG(path, pallet, is_draw_encoding) -> None:
    fig, ax = plt.subplots()
    image_size(fig, pallet.expand_pallet.size)
    focusing_on_subject(ax, pallet.original_pallet.minXY(),
                        pallet.original_pallet.maxXY())
    draw_polygon(ax, pallet.expand_pallet, 'green')
    draw_polygon(ax, pallet.original_pallet)
    if is_draw_encoding:
        draw_compressed_encoding(ax, pallet.expand_pallet.minXY(),
                                 pallet.compressed_encoding, pallet.__eps)
    for position in pallet.plased_items_positions:
        draw_polygon(ax, position.polygon_on_position, 'black')
    plt.savefig(path[:-4] + '-' + str(pallet.id) + '.png')


def save_as_PNG(path, packing, is_draw_encoding=False) -> None:
    for pallet in packing.pallets:
        save_pallet_as_PNG(path, pallet, is_draw_encoding)