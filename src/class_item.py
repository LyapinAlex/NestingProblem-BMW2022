import math
import time
import random
import numpy as np
from matplotlib import patches
from matplotlib import pyplot as plt

from smth2matrix.polygon2matrix import polygon2matrix
from smth2matrix.polyline2matrix import polyline2matrix
from smth2matrix.shift2zero import shift2zero
from shift_code.simple2mixed_shift import simple2mixed_shift
from preprocess.expand_polygon import expand_polygon

class Item:

    def __init__(self,
                 id: int,
                 points: list):
        self.id = id
        self.points = points

        self.matrix = None
        self.list_matrix = None

        self.lb_x = None
        self.lb_y = None
        self.rotation = 0.0
        self.pallet_number = None

    def clear_coordinat(self):
        self.lb_x = None
        self.lb_y = None
        self.rotation = 0.0
        self.pallet_number = None
        return None


    def set_rectangular_matrix(self, h):
        """Приближение объекта описанным прямоугольником"""
        x_max, y_max = np.amax(self.shell_points, axis = 0)
        x_min, y_min = np.amin(self.shell_points, axis = 0)

        self.matrix = np.ones((math.ceil(
            (x_max - x_min) / h), math.ceil((y_max - y_min) / h)),
                              dtype="int")
        return None


    def set_matrix(self, h):
        """Приближение объекта пиксельным способом, с размером пискля - h"""
        self.matrix = polygon2matrix(self.shell_points, h)
        return None


    def matrix_of_border(self, h):
        """Приближение границы объекта пиксельным способом, с размером пискля - h"""
        mat = polyline2matrix(self.shell_points, h)
        return mat

    def rotationMatrix(self):
        # self.rotation = math.ceil(rotate / math.pi * 90)
        # if (self.rotation % 90 == 0):
        #     self.matrix = np.rot90(self.matrix, self.rotation // 90)
        # else:
        #     print("Не прямой поворот:", self.rotation)
        self.matrix = np.rot90(self.matrix)
        return None


    def list_of_MixedShiftC_4R(self, h):  # крутит против часовой стрелки
        """
        Приближение объекта пиксельным способом (кодировкой с переходом), с размером пискля - h
        
        Returns:
            np.array[4]: содержит 4 поворота текущего объекта в формате кодировки с переходом
        """

        if self.empty_matrix():
            self.set_matrix(h)

        li = np.array([None, None, None, None])
        for i in range(0, 4):
            li[i] = np.rot90(simple2mixed_shift(np.rot90(self.matrix, 3 + i)))
            # li[i] = simple2mixed_shift(np.rot90(self.matrix, i ))
        self.list_matrix = li
        return None

    
    def empty_matrix(self):
        return self.matrix == None #!фигню написал, удалить


    def shift2zero(self):
        """Перемещает объект в первую координатную четверть, вниз влево"""
        return shift2zero(self.shell_points)


    def draw_polygon(self, h, code_type = 0):
        """
        Отрисовывает объект с его пиксельным приближением 
        code_type = 0: простая кодировка (по умолчанию)
        code_type = 1: кодировка со сдвигом
        """
        fig, ax = plt.subplots()
        MAX_SIZE = 7
        if self.matrix.shape[0] > self.matrix.shape[1]:
            fig.set_figheight(MAX_SIZE * self.matrix.shape[1]/self.matrix.shape[0])
            fig.set_figwidth(MAX_SIZE)
        else:
            fig.set_figheight(MAX_SIZE)
            fig.set_figwidth(MAX_SIZE * self.matrix.shape[0]/self.matrix.shape[1])
    
        pallet = patches.Rectangle((0, 0), h*self.matrix.shape[0], h*self.matrix.shape[1], linewidth=2, facecolor='none', edgecolor='black')
        ax.add_patch(pallet)
        ax.set_xlim(-1, h*self.matrix.shape[0] + 1)
        ax.set_ylim(-1, h*self.matrix.shape[1] + 1)

        if not code_type:
            random_color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for j in range(self.matrix.shape[1]):
                for i in range(self.matrix.shape[0]):
                    if self.matrix[i][j]:
                        sqver = np.array([[i, j], [i+1, j], [i+1, j+1], [i, j+1]])*h
                        polygon = patches.Polygon(sqver, linewidth=1, facecolor=random_color, edgecolor='black', alpha = 0.33)
                        ax.add_patch(polygon)
        else:
            max_pl = np.amax(self.list_matrix[0])
            min_otr = np.amin(self.list_matrix[0])*(-1)
            cmapin = plt.cm.get_cmap('Blues', max_pl)
            cmapout = plt.cm.get_cmap('Reds', min_otr)

            for j in range(self.list_matrix[0].shape[1]):
                for i in range(self.list_matrix[0].shape[0]):
                    if self.list_matrix[0][i][j] > 0:
                        sqver = np.array([[i, j], [i+1, j], [i+1, j+1], [i, j+1]])*h
                        polygon = patches.Polygon(sqver, linewidth=1, edgecolor='black', facecolor = cmapin(self.list_matrix[0][i][j]))
                        ax.add_patch(polygon)
                    else:
                        sqver = np.array([[i, j], [i+1, j], [i+1, j+1], [i, j+1]])*h
                        polygon = patches.Polygon(sqver, linewidth=1, edgecolor='black', facecolor = cmapout(self.list_matrix[0][i][j]*(-1)))
                        ax.add_patch(polygon)
        
        polygon = patches.Polygon(self.shell_points, linewidth=1, edgecolor='red', fill = False)
        ax.add_patch(polygon)
        plt.show()
        return None

    def creat_polygon_shell(self, drill_radius):
        """
        Создает облочку вокруг предмета с отсупом в drill_radius.
        Перемещает фигуры и ее фигуру в первую координатную четверть, сохраняя корректное расположение фигуры внутри своей оболочки.
        Инициализирует в Item атрибуты:
        shell_points - точки описывающие оболочку
        """


        x_min_pol, y_min_pol = np.amin(self.points, axis = 0)
        self.shell_points = expand_polygon(self.points, drill_radius)
        x_min_shell, y_min_shell = np.amin(self.shell_points, axis = 0)
        vector_surf = np.array([x_min_pol - x_min_shell, y_min_pol - y_min_shell])
        shift2zero(self.shell_points)
        shift2zero(self.points)

        for point in self.points:
            point+=  vector_surf

        return None


if (__name__=='__main__'):
    h = 0.1

    # start_time = time.time()
    eq1 = Item(1, np.array([[0.3, 0.5], [0, 1], [0.7, 1.5], [1.2, 0.8], [3, 0.8], [3, 0.4], [1.2, 0.4], [0.6, 0.8]]))
    eq1.set_matrix(h)
    print(eq1.matrix)
    # eq1.list_of_MixedShiftC_4R(h)
    # print(time.time() - start_time, " seconds")

    # print(int(eq1.matrix.shape[0]))
    # eq1.draw_polygon(h)
