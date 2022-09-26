from data_rendering.drow_pallet_with_polygons import drow_pallet_with_polygons
from putting_data.txt2polygons import txt2polygons


def main():
    num_pallets = 1
    for i in range(num_pallets):
        print(123)
        polygons = txt2polygons(r'src\input\test' + str(i) + '.txt')
        drow_pallet_with_polygons(
            polygons, 2000, 2000,
            r'src\output\pallet' + str(i) + '_from_cpp.png')


if __name__ == "__main__":
    main()