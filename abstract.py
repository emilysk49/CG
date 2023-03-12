from abc import ABC, abstractmethod
from enum import Enum

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
