from class_packing import Packing


def main():
    packaging = Packing(width=2000,
                        height=1000,
                        drill_radius=2,
                        border_distance=2.1)

    packaging.packing_from_file(input_file_name='NEST001-108.dxf',
                                output_file_name='pallet.png',
                                eps=10)
    return None


if __name__ == '__main__':
    main()
