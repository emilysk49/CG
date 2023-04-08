from abstract import ObjetoGrafico, Tipo
import numpy as np

class Window(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas=[(-11,-11), (11,-11), (11,11), (-11,11)]):
        super().__init__(nome, Tipo.WIN.value, coordenadas)
        self.BE = (-11, -11) #min
        self.BD = (11, -11)
        self.CD = (11, 11) #max
        self.CE = (-11, 11)
        self.cor = "#ffffff"
        self.coordNorm = [(-1,-1), (1,-1), (1,1), (-1,1)] #BE BD CD CE
        self.angulo = 0

        self.max_min()

    def moverXY(self, mat):
        self.coordenadas = self.mulPontoMat(mat)
        self.BE = self.coordenadas[0]
        self.BD = self.coordenadas[1]
        self.CD = self.coordenadas[2]
        self.CE = self.coordenadas[3]
        self.calc_centro()

        self.max_min()
        

            
    def normalize(self, mat: np.matrix):
        self.coordNorm = self.mulPontoMat(mat)


    def max_min(self):
        self.xmax = self.coordenadas[0][0]
        self.xmin = self.coordenadas[0][0]
        self.ymax = self.coordenadas[0][1]
        self.ymin = self.coordenadas[0][1]
        for i in self.coordenadas:
            if i[0] > self.xmax:
                self.xmax = i[0]
            if i[0] < self.xmin:
                self.xmin = i[0]
            if i[1] > self.ymax:
                self.ymax = i[1]
            if i[1] < self.ymin:
                self.ymin = i[1]