from abstract import ObjetoGrafico, Tipo
import numpy as np

class Window(ObjetoGrafico):
    #Caso defina coordenadas da window (RETANGULAR) por favor siga a ordem das coordenadas: primeira -> Baixo esquerda, 
                                                                                            #segunda -> baixo direita, 
                                                                                           #terceira -> cima direita, 
                                                                                             #quarta -> cima esquerda
    def __init__(self, nome, coordenadas=[(-11,-11,0), (11,-11,0), (11,11,0), (-11,11,0)]):
        super().__init__(nome, Tipo.WIN.value, coordenadas)
        self.BE = coordenadas[0]#(-11, -11, 0) #min
        self.BD = coordenadas[1]#(11, -11, 0)
        self.CD = coordenadas[2]#(11, 11, 0) #max
        self.CE = coordenadas[3]#(-11, 11, 0)
        self.cor = "#ffffff"
        self.coordNorm = [(-1,-1), (1,-1), (1,1), (-1,1)] #BE BD CD CE
        self.angulo = float()
        self.contagem = 0
        self.centroHomo = list()
        self.centroXHomo = float()
        self.centroYHomo = float()
        self.centroZHomo = float()
        self.escalaX = float()
        self.escalaY = float()


    def moverXY(self, mat, homo=False):
        super().moverXY(mat, homo)
        if not homo:
            self.BE = self.coordenadas[0]
            self.BD = self.coordenadas[1]
            self.CD = self.coordenadas[2]
            self.CE = self.coordenadas[3]
            self.calc_centro()

        self.calc_centro_homo()
        #print(f"As coordenadas da window são: {self.coordenadas}")



    def calc_angulo(self):
        px = (self.coordHomo[2][0] + self.coordHomo[3][0]) /2 #ponto central de cima x
        py = (self.coordHomo[2][1] + self.coordHomo[3][1]) /2 #ponto central de cima y
        self.vup = (px-self.centroXHomo, py-self.centroYHomo) #vetor para cima do window
        #print(f"VUP: {self.vup}")
        y = [0,1]
        
        #produto_escalar = np.dot(self.vup, y)
        
        # Calcule o produto escalar e o determinante
        dot = np.dot([self.vup[0], self.vup[1]], [0, 1])
        det = np.cross([self.vup[0], self.vup[1]], [0, 1])

        # Calcule o ângulo em radianos
        angle = np.arctan2(det, dot)

        # Converta o ângulo para graus
        self.angulo = np.degrees(angle)

        #norma_cima = np.linalg.norm(self.vup)
        #norma_y = np.linalg.norm(y)

        #self.angulo = np.degrees(np.arccos(produto_escalar / (norma_cima * norma_y)))

        #if px < 0:
        #    self.angulo = 360 - self.angulo

        #print(self.angulo)

            

    def calc_centro_homo(self):
        n = len(self.coordHomo)
        x, y, z = 0, 0, 0
        for i in range (0, n):
            x += self.coordHomo[i][0]
            y += self.coordHomo[i][1]
            z += self.coordHomo[i][2]
        self.centroXHomo = x/n
        self.centroYHomo = y/n
        self.centroZHomo = z/n
        self.centroHomo = [self.centroXHomo, self.centroYHomo, self.centroZHomo]
