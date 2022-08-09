
from UnderstandPallets import understand_pallets
from PalletQuality import pallet_quality


def packing_quality(items, eps):
    quality = 0
    pallets = understand_pallets(items)
    for pallet in pallets:
        quality += pallet_quality(pallet, eps)
    return quality
