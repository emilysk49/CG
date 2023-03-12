from abstract import ObjetoGrafico, Tipo

class Polygon(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas):
        super().__init__(nome, Tipo.POLYGON.value, coordenadas)
