from abstract import ObjetoGrafico, Tipo
import numpy as np

class Polygon(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas):
        super().__init__(nome, Tipo.POLYGON.value, coordenadas)
        self.cor = "#7600d0"

    def moverXY(self, mat):
        resposta = []
        for i in self.coordenadas:
            x = i[0]
            y = i[1]
            ponto = [x,y,1]
            result = np.matmul(ponto, mat)
            resposta.append((result.item(0),result.item(1)))
        self.coordenadas = resposta
            
            