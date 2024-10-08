from abc import ABC, abstractmethod
from enum import Enum
import numpy as np

class Tipo(Enum):
    POINT = 1
    LINE = 2
    POLYGON = 3
    WIN = 4
    CURVE = 5
    ARAME = 6
    SUPERFICIE = 7
    SUPERFICIEB = 8


class ObjetoGrafico(ABC):

    @abstractmethod
    def __init__(self, nome: str, tipo: Tipo, coordenadas: list):
        self._nome = nome
        self._tipo = tipo
        self._coordenadas = coordenadas
        self.centroX = float()
        self.centroY = float()
        self.centroZ = float()
        self.centro = float()
        self.coordNorm = list()
        self.coordHomo = list()
        self._cor = str
        self.calc_centro()
    
        

    @property
    def cor(self):
        return self._cor
    
    @cor.setter
    def cor(self, nome):
        self._cor = nome

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, n):
        self._nome = n

    @property
    def coordenadas(self):
        return self._coordenadas

    @coordenadas.setter
    def coordenadas(self, coord):
        self._coordenadas = coord

    @property
    def tipo(self):
        return self._tipo

    def calc_centro(self):
        n = len(self._coordenadas)
        x, y, z = 0, 0, 0
        for i in range (0, n):
            x += self._coordenadas[i][0]
            y += self._coordenadas[i][1]
            z += self._coordenadas[i][2]
        self.centroX = x/n
        self.centroY = y/n
        self.centroZ = z/n
        self.centro = (self.centroX, self.centroY, self.centroZ)
    
    def moverXY(self, mat: np.matrix, homo=False):
        if homo:
            self.coordHomo = self.mulPontoMat3D(mat)
            return
        self.coordenadas = self.mulPontoMat3D(mat)
        self.calc_centro()

    def normalize(self, mat: np.matrix):
        pass

    def mulPontoMat2D(self, mat):
        resposta = []
        for i in self.coordHomo:
            x = i[0]
            y = i[1]
            ponto = [x,y,1]
            result = np.matmul(ponto, mat)
            resposta.append((result.item(0),result.item(1)))
        return resposta
    
    def mulPontoMat3D(self, mat):
        resposta = []
        for i in self.coordenadas:
            x = i[0]
            y = i[1]
            z = i[2]
            ponto = [x,y,z,1]
            result = np.matmul(ponto, mat)
            resposta.append((result.item(0),result.item(1),result.item(2)))
        return resposta

    def projete(self, mat):
        for i in range(len(self.coordHomo)):
            homo = [self.coordHomo[i][0], self.coordHomo[i][1], self.coordHomo[i][2], 1]
            resp = np.matmul(homo, mat)
            x = resp.item(0)
            y = resp.item(1)
            z = resp.item(2)
            w = resp.item(3)
            self.coordHomo[i] = [x/w, y/w, z/w]


    def export(self):
        exp = {}
        exp["nome"] = self.nome 
        exp["coord"] = self.coordenadas
        exp["cor"] = self.cor
        exp["tipo"] = self.tipo

        return exp
        
