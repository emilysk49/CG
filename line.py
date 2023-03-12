from abstract import ObjetoGrafico, Tipo

class Line(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas):
        super().__init__(nome, Tipo.LINE.value, coordenadas)