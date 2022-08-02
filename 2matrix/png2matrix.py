import numpy as np
from PIL import Image

def png2matrix(img): # ввод: сырая ссылка на объект png2matrix(r"2matrix/chel.png")
    numpydata = np.asarray(Image.open(img))
    matrix = np.ones((numpydata.shape[0], numpydata.shape[1]), dtype="int")
    for i in range(0, numpydata.shape[0]):
        for j in range(0, numpydata.shape[1]):
            if (numpydata[i][j][0] == 255 and numpydata[i][j][1] == 255
                    and numpydata[i][j][2] == 255):
                matrix[i][j] = 0
    return matrix

# print(png2matrix(r"2matrix/chel.png"))