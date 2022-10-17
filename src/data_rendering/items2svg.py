def items2svg(save_path, items, packaging, indent):
    w = packaging.pallet_width + 2 * indent
    h = packaging.pallet_height + 2 * indent
    f = open(save_path[:-4] + str(items[0].pallet_id) + '.svg', 'w')
    f.write(
        "<svg x=\"%g\" y=\"%g\" width=\"%g\" height=\"%g\" viewBox=\"%g %g %g %g\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"> "
        % (-indent, -indent, w, h, -10 - indent, -10 - indent, w + 10, h + 10) + '\n')
    # <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
    f.write(
        "<rect x=\"%g\" y=\"%g\" width=\"%g\" height=\"%g\" style=\"stroke:#000000; stroke-width:0.72; fill:none\" />"
        % (-indent, -indent, w, h) + '\n')
    for item in items:
        d = ' '.join([
            '%s%g %g' % (['M', 'L'][i > 0], x, y)
            for i, (x, y) in enumerate(item.points)
        ])
        f.write(
            "<path style=\"stroke:#000000; stroke-width:0.72; fill:none\"  d=\""
            + d + "Z\"/>" + '\n')

    f.write("</svg>")
    f.close()
    return
