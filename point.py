from abstract import ObjetoGrafico, Tipo
import numpy as np

class Point(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas):
        super().__init__(nome, Tipo.POINT.value, coordenadas)
        self.cor = "#ff0000"

    def moverXY(self, mat):
        x = self.coordenadas[0][0]
        y = self.coordenadas[0][1]
        ponto = [x,y,1]
        result = np.matmul(ponto, mat)

        self.coordenadas = [(result.item(0), result.item(1))]

        self.calc_centro()
