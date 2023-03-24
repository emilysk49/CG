from abc import ABC, abstractmethod
from enum import Enum
import numpy

class Tipo(Enum):
    POINT = 1
    LINE = 2
    POLYGON = 3

class ObjetoGrafico(ABC):

    @abstractmethod
    def __init__(self, nome: str, tipo: Tipo, coordenadas: list):
        self._nome = nome
        self._tipo = tipo
        self._coordenadas = coordenadas
        self.centroX = float()
        self.centroY = float()
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
    
    def moverXY(self, mat: numpy.matrix):
        pass

