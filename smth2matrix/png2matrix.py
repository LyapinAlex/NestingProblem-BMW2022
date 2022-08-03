import numpy as np
from PIL import Image


def png2matrix(image_path, h):
    # ввод: сырая ссылка на объект png2matrix(r"smth2matrix/input/head.png", 0.5)
    img = Image.open(image_path)
    w_size = int(img.size[0] / h)
    h_size = int(img.size[0] / h)
    new_img = img.resize((w_size, h_size))
    numpydata = np.asarray(new_img)
    matrix = np.ones((numpydata.shape[0], numpydata.shape[1]), dtype="int")
    for i in range(0, numpydata.shape[0]):
        for j in range(0, numpydata.shape[1]):
            if (numpydata[i][j][0] == 255 and numpydata[i][j][1] == 255
                    and numpydata[i][j][2] == 255):
                matrix[i][j] = 0
    return matrix


# print(png2matrix(r"smth2matrix/input/head.png", 0.5))