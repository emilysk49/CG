from abstract import ObjetoGrafico, Tipo
import numpy as np

class Polygon(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas):
        super().__init__(nome, Tipo.POLYGON.value, coordenadas)
        self.cor = "#7600d0"
        self.coordClip = []

    def moverXY(self, mat):
        self.coordenadas = self.mulPontoMat(mat)
        self.calc_centro()
            
    def normalize(self, mat: np.matrix):
        self.coordNorm = self.mulPontoMat(mat)

    