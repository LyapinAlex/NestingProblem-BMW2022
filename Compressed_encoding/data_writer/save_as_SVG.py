def save_pallet_as_SVG(path, pallet) -> None:
    f = open(path[:-4] + '-' + str(pallet.id) + '.svg', 'w')
    pal_points = pallet.original_pallet.points_to_list()
    pal_width = pal_points[2][0] - pal_points[0][0]
    pal_height = pal_points[2][1] - pal_points[0][1]
    params = (pal_points[0][0], pal_points[0][1], pal_width, pal_height,
              pal_points[0][0] - 10, pal_points[0][1] - 10, pal_width + 10,
              pal_height + 10)
    f.write(
        "<svg x=\"%g\" y=\"%g\" width=\"%g\" height=\"%g\" viewBox=\"%g %g %g %g\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"> "
        % params + '\n')

    d = ' '.join([
        '%s%g %g' % (['M', 'L'][i > 0], x, -y + pal_height)
        for i, (x, y) in enumerate(pal_points)
    ])
    f.write(
        "<path style=\"stroke:#000000; stroke-width:0.72; fill:none\"  d=\"" +
        d + "Z\"/>" + '\n')

    for position in pallet.plased_items_positions:
        points = position.polygon_on_position.points_to_list()
        d = ' '.join([
            '%s%g %g' % (['M', 'L'][i > 0], x, -y + pal_height)
            for i, (x, y) in enumerate(points)
        ])
        f.write(
            "<path style=\"stroke:#000000; stroke-width:0.72; fill:none\"  d=\""
            + d + "Z\"/>" + '\n')

    f.write("</svg>")
    f.close()
    return


def save_as_SVG(path, packing) -> None:
    for pallet in packing.pallets:
        save_pallet_as_SVG(path, pallet)