from abstract import ObjetoGrafico, Tipo
import numpy as np

class Line(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas):
        super().__init__(nome, Tipo.LINE.value, coordenadas)
        self.cor = "#0000ff"

    def moverXY(self, mat):
        x1 = self.coordenadas[0][0]
        y1 = self.coordenadas[0][1]

        x2 = self.coordenadas[1][0]
        y2 = self.coordenadas[1][1]

        p1 = [x1, y1, 1]
        p2 = [x2, y2, 1]


        p1 = np.matmul(p1, mat)
        p2 = np.matmul(p2, mat)


        self.coordenadas = [(p1.item(0),p1.item(1)), (p2.item(0), p2.item(1))] 

        self.calc_centro()