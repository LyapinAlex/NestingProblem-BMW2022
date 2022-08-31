from svg.path import parse_path
from svg.path.path import Line
from xml.dom import minidom
import numpy as np

def svg_paths2polygons(file_name):
    # read the SVG file
    doc = minidom.parse(file_name)
    path_strings = [path.getAttribute('d') for path
                    in doc.getElementsByTagName('path')]
    doc.unlink()

    list_of_items = []
    # print the line draw commands
    for path_string in path_strings:
        path = parse_path(path_string)
        polygon = []
        for e in path:
            if isinstance(e, Line):
                polygon.append([e.start.real, e.start.imag])
        list_of_items.append(np.array(polygon))
    
    return np.array(list_of_items)

if __name__=='__main__':
    print(svg_paths2polygons('test1.svg'))