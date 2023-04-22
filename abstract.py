from abc import ABC, abstractmethod
from enum import Enum
import numpy as np

class Tipo(Enum):
    POINT = 1
    LINE = 2
    POLYGON = 3
    WIN = 4
    CURVE = 5

class ObjetoGrafico(ABC):

    @abstractmethod
    def __init__(self, nome: str, tipo: Tipo, coordenadas: list):
        self._nome = nome
        self._tipo = tipo
        self._coordenadas = coordenadas
        self.centroX = float()
        self.centroY = float()
        self.coordNorm = list()
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
        x, y = 0, 0
        for i in range (0, n):
            x += self._coordenadas[i][0]
            y += self._coordenadas[i][1]
        self.centroX = x/n
        self.centroY = y/n
    
    def moverXY(self, mat: np.matrix):
        pass

    def normalize(self, mat: np.matrix):
        pass

    def mulPontoMat(self, mat):
        resposta = []
        for i in self.coordenadas:
            x = i[0]
            y = i[1]
            ponto = [x,y,1]
            result = np.matmul(ponto, mat)
            resposta.append((result.item(0),result.item(1)))
        return resposta

    def export(self):
        exp = {}
        exp["nome"] = self.nome 
        exp["coord"] = self.coordenadas
        exp["cor"] = self.cor
        exp["tipo"] = self.tipo

        return exp
        
