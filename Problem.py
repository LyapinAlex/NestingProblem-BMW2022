# import sys
# sys.path.append('./data')
import localSearch
import generate
import rastr_method
import pallet
import copy

w = 10
l = 10
n = 50
e = 1

class Problem():
    #  иницализация задчи, задание длины, ширины, количества элементов
    def __init__(self, name="", len = l, width = w, number = n):
        self.len = len
        self.width = width
        self.number = number

        self.setOfPlane = []
        self.data = None
        self.pallet = pallet.Pallet(0 ,w, l, e)
    

    def generatData(self):
        g = generate.Generator(w,l, n)
        g.start(e)
        self.data = g.data
        

    def rastrMethod(self):

        print(len(rastr_method.fit_pallets(self.pallet.matrix, self.data)))

    def localSearch(self):

        self.data = localSearch.locSearch(self.pallet.matrix, copy.deepcopy(self.data))
        
        print(len(rastr_method.fit_pallets(self.pallet.matrix, self.data)))


# p = Problem()
# p.generatData()
# p.localSearch()



