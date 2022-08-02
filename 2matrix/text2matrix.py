from PIL import Image, ImageDraw, ImageFont
import numpy as np


def make_unicode(inp):
    if type(inp) != type('1'):
        inp = inp.decode('utf-8')
    return inp


def text2matrix(text, size,
                fon):  # size - размер шрифта в пикселях; fon - имя шрифта
    unicode_text = make_unicode(text)
    font = ImageFont.truetype(fon, size, encoding="unic")
    text_width, text_height = font.getsize(unicode_text)
    canvas = Image.new('RGB', (text_width, text_height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((0, 0), unicode_text, 'black', font)

    numpydata = np.asarray(canvas)
    matrix = np.ones((numpydata.shape[0], numpydata.shape[1]), dtype="int")
    for i in range(0, numpydata.shape[0]):
        for j in range(0, numpydata.shape[1]):
            if (numpydata[i][j][0] == 255 and numpydata[i][j][1] == 255
                    and numpydata[i][j][2] == 255):
                matrix[i][j] = 0
    return matrix


# st1 = "No 9"
# st2 = "No2"
# fon1 = "HARNGTON.TTF"
# fon2 = "KUNSTLER.TTF"
# id1 = 121
# id2 = 16
# size1 = 50
# size2 = 20

# print(text2matrix(id1, st2, size2, fon2))