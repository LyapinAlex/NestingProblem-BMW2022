from PIL import Image, ImageDraw, ImageFont
import numpy as np

# from cairosvg import svg2png
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPM


def make_unicode(inp):
    if type(inp) != type(u"a"):
        inp = inp.decode('utf-8')
    return inp


def png2matrix(img):
    numpydata = np.asarray(img)
    matrix = np.ones((numpydata.shape[0], numpydata.shape[1]), dtype="int")
    for i in range(0, numpydata.shape[0]):
        for j in range(0, numpydata.shape[1]):
            if (numpydata[i][j][0] == 255 and numpydata[i][j][1] == 255
                    and numpydata[i][j][2] == 255):
                matrix[i][j] = 0
    return matrix


# def svg2matrix(id):
#     # svg2png(bytestring=svg_code, write_to=)
    
#     drawing = svg2rlg('loopa.svg')
#     renderPM.drawToFile(drawing, "125.png", fmt='PNG')
#     return None


def text2matrix(st, size, fon, id):
    unicode_text = make_unicode(st)
    font = ImageFont.truetype(fon, size, encoding="unic")
    text_width, text_height = font.getsize(unicode_text)
    canvas = Image.new('RGB', (text_width, text_height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((0, 0), unicode_text, 'black', font)
    name = r"png2matrix\\" + str(id) + ".png"
    canvas.save(name, "PNG")
    print(canvas)
    # canvas.show()
    return png2matrix(canvas)


st1 = "No 9"
fon1 = "HARNGTON.TTF"
fon2 = "KUNSTLER.TTF"
id1 = 121
id2 = 16
size1 = 50

# print(svg2matrix(id2))
# print(text2matrix(st1, size1, fon2, id1))
# print(png2matrix(Image.open(r"png2matrix\\" + str(125) + ".png")))
print(png2matrix(Image.open(r"png2matrix/chel.png")))