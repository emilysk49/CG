from abstract import ObjetoGrafico, Tipo
import numpy as np

class Line(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas):
        super().__init__(nome, Tipo.LINE.value, coordenadas)
        self.cor = "#0000ff"

    def moverXY(self, mat):
        self.coordenadas = self.mulPontoMat(mat)

        self.calc_centro()

    def normalize(self, mat: np.matrix):
        self.coordNorm = self.mulPontoMat(mat)


