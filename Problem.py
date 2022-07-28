import sys
sys.path.append('./data')

import generate

import rastr_method

w = 100
l = 100
n = 10
class Problem():

    def __init__(self, name="", len = l, width = w, number = n):
        self.len = len
        self.width = width
        self.number = number

        self.solution = []
        self.data = []
        self.order = range(n)

        self.objFun = int("inf")
    
    def generateData(self):

        g = generate.Generator(w, l, n)
        g.start()
        self.data = g.data
    

    def rasateMetdod(self):

        usePallet = rast(data)
        if 
        pass






