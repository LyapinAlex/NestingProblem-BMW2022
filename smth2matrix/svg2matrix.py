from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


if __name__=='__main__':
    from png2matrix import png2matrix
else:
    from .png2matrix import png2matrix



def svg2matrix(svg_file, h):
    # ввод: сырая ссылка на объект png2matrix(r"smth2matrix/input/head.png", 0.5)
    open(svg_file, 'r', encoding='utf-8').read()
    drawing = svg2rlg(svg_file)
    output = r'smth2matrix/output/primer.png'
    renderPM.drawToFile(drawing, output, fmt='PNG')
    return png2matrix(output, h)

if (__name__=='__main__'):
    print(svg2matrix(r'smth2matrix/input/ice.svg', 5))