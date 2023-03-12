from abstract import ObjetoGrafico, Tipo

class Point(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas):
        super().__init__(nome, Tipo.POINT.value, coordenadas)
