from abstract import ObjetoGrafico, Tipo
import numpy as np

class Point(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas):
        super().__init__(nome, Tipo.POINT.value, coordenadas)
        self.cor = "#ff0000"

    def moverXY(self, mat):
        self.coordenadas = self.mulPontoMat(mat)
        self.calc_centro()

    def normalize(self, mat: np.matrix):
        self.coordNorm = self.mulPontoMat(mat)

