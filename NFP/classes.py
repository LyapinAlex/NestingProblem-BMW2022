import numpy as np

class Vertex:
    def __init__(self, coordinate, edges = None):
        """
        Args:
            coordinate(np.array):
                две координаты (real) вершины
            edges( list( list( vertex, np.array ) ) ):
                список соседних вершин (vertex) и единичных нормалей (np.array), каждая из которых
                ортогональна к соответствующей стороне (образованной из текщей и соседней вершиной)
                и направлена в сторону пустоты предмета
        """
        self.coordinate = coordinate
        self.edges = edges
    
    def get_neighboring_vertex(self, num = 0):
        return self.edges[num][0]

if __name__=='__main__':
    p1 = Vertex(np.array([0,0]))
    p2 = Vertex(np.array([1.2,0]), [[p1, np.array([7,7])]])
    nei = p2.get_neighboring_vertex()
    nei.coordinate = np.array([-1,-1])
    print(p1.coordinate)
    # print((p2.edges[0][0]).coordinate)
    # print(p2.get_neighboring_vertex())