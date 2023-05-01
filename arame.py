from abstract import ObjetoGrafico, Tipo
from line import Line
import numpy as np

class Arame(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, obj_list):
        self.obj_list = obj_list
        self.cor = "#fc8403"
        super().__init__(nome, Tipo.ARAME.value, "Objeto arame não possui coordenadas próprias")

    @ObjetoGrafico.cor.setter
    def cor(self, valor):
        self._cor = valor
        for obj in self.obj_list:
            obj.cor = valor
            
    def normalize(self, mat: np.matrix):
        #print(self.obj_list)
        for obj in self.obj_list:
            obj.normalize(mat)
  
    def calc_centro(self):
        sumX, sumY, sumZ = 0,0,0
        tam = len(self.obj_list)
        for i in range(tam):
            sumX += self.obj_list[i].centroX
            sumY += self.obj_list[i].centroY
            sumZ += self.obj_list[i].centroZ
            
        self.centroX = sumX/tam
        self.centroY = sumY/tam
        self.centroZ = sumZ/tam
        self.centro = (self.centroX, self.centroY, self.centroZ)

    def moverXY(self, mat: np.matrix, homo=False):
        for obj in self.obj_list:
            if homo:
                obj.coordHomo = obj.mulPontoMat3D(mat)
                continue
            obj.coordenadas = obj.mulPontoMat3D(mat)
            obj.calc_centro()
        self.calc_centro()

    def arame_clipping(self, clipeLinha):
        for obj in self.obj_list:
            if obj.tipo == 1:
                obj.ponto_clipping()
            elif obj.tipo == 2:
                if clipeLinha == "l":
                    obj.liang_barsky()
                else:
                    obj.cohen_sutherland()
            elif obj.tipo == 5:
                obj.curv_clipping()
                

    
    def mulPontoMat2D(self, mat):
        print("Está chamando mulPontoMat2D para um objeto ARAME, abortando")
        exit()
    
    def mulPontoMat3D(self, mat):
        print("Está chamando mulPontoMat3D para um objeto ARAME, abortando")
        exit()
    
    def export(self):
        print("A finalizar para objetos ARAME")
