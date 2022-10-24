from class_packing import Packing


def main():
    packaging = Packing(width=2000,
                        height=1000,
                        drill_radius=2,
                        border_distance=2.1)

    packaging.packing_from_file(input_file_name='NEST003-432.dxf',
                                output_file_name='pallet.png',
                                eps=5.75)
    return None


if __name__ == '__main__':
    main()
