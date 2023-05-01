from abstract import ObjetoGrafico, Tipo
import numpy as np

class Point(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas):
        super().__init__(nome, Tipo.POINT.value, coordenadas)
        self.cor = "#ff0000"
        self.desenhavel = bool

    def normalize(self, mat: np.matrix):
        self.coordNorm = self.mulPontoMat2D(mat)

    def ponto_clipping(self):
        if (self.coordNorm[0][0] < -1 or self.coordNorm[0][0] > 1 or
            self.coordNorm[0][1] < -1 or self.coordNorm[0][1] > 1):
            self.desenhavel = False
        else:
            self.desenhavel = True

