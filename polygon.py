from abstract import ObjetoGrafico, Tipo
from line import Line
import numpy as np

class Polygon(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas):
        super().__init__(nome, Tipo.POLYGON.value, coordenadas)
        self.cor = "#7600d0"
        self.coordClip = []

    def moverXY(self, mat):
        self.coordenadas = self.mulPontoMat(mat)
        self.calc_centro()
            
    def normalize(self, mat: np.matrix):
        self.coordNorm = self.mulPontoMat(mat)

    def weiler_atherton(self):                #Inspirado em weiler-atherton, mas refizemos algumas partes conforme consideramos mais simples
        coord = []                                          #Andamos em cada ponto avaliando 
        for i in range(len(self.coordNorm)):
            p1 = self.coordNorm[i-1]
            p2 = self.coordNorm[i]
            if (p1[0] <= 1 and p1[0] >= -1 and p1[1] <= 1 and p1[1] >= -1 and #Se p1 está na window
                p2[0] <= 1 and p2[0] >= -1 and p2[1] <= 1 and p2[1] >= -1):   #Se p2 está na window
                if (not coord) or coord[-1] != p1 :                           #Se nao eh primeiro da lista ou se ultimo nao eh p1 (cuidar pra nao incluir de novo)
                    coord.append( (p1, False) )   
                coord.append((p2, False) )
            elif (p1[0] <= 1 and p1[0] >= -1 and p1[1] <= 1 and p1[1] >= -1): #Se apenas p1 está na window
                if (not coord) or coord[-1] != p1:                            #Se nao eh primeiro da lista ou se ultimo nao eh p1 (cuidar pra nao incluir de novo)
                    coord.append((p1, False))                                 #Logo, p2 tem intersecção
                l = Line("_________", [p1,p2])
                l.coordNorm = [p1, p2]
                l.liang_barsky()
                coord.append((l.coordClip[1], "s"))                           # "s" indica que eh sainte
            elif (p2[0] <= 1 and p2[0] >= -1 and p2[1] <= 1 and p2[1] >= -1): #Se apenas p2 está na window
                l = Line("_________", [p1,p2])
                l.coordNorm = [p1, p2]
                l.liang_barsky()
                if (not coord) or coord[-1] != l.coordClip[0]:                #Se nao eh primeiro da lista ou se ultimo nao eh mesma interseccao 
                    coord.append((l.coordClip[0], "e"))                       # "e" indica que eh entrante
                coord.append((p2, False))                                     #Logo, p1 tem intersecção
        
            else:                                                             #Se nenhum deles está dentro da windo
                l = Line("_________", [p1,p2])
                l.coordNorm = [p1, p2]
                l.liang_barsky()
                if l.desenhavel:                                              #Caso tenha intersecção
                    if (not coord) or (coord[-1] != l.coordClip[0]):          #Se nao eh primeiro da lista ou se ultimo nao eh mesma interseccao 
                        coord.append( (l.coordClip[0], "e") )                 # "e" indica que eh entrante
                    coord.append( (l.coordClip[1], "s") )                     # "s" indica que eh sainte
                else:
                    coord.append(())

        self.coordClip = coord



    