from abstract import ObjetoGrafico, Tipo
import numpy as np

class Win(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas=[(-11,-11), (11,-11), (11,11), (-11,11)]):
        super().__init__(nome, Tipo.WIN.value, coordenadas)
        self.BE = (-11, -11)
        self.BD = (11, -11)
        self.CD = (11, 11)
        self.CE = (-11, 11)
        self.cor = "#ffffff"
        self.coordNorm = [(-1,-1), (1,-1), (1,1), (-1,1)] #BE BD CD CE
        self.angulo = 0

    def moverXY(self, mat):
        self.coordenadas = self.mulPontoMat(mat)
        self.BE = self.coordenadas[0]
        self.BD = self.coordenadas[1]
        self.CD = self.coordenadas[2]
        self.CE = self.coordenadas[3]
        self.calc_centro()
            
    def normalize(self, mat: np.matrix):
        self.coordNorm = self.mulPontoMat(mat)
