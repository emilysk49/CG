from abstract import ObjetoGrafico, Tipo
from line import Line
import numpy as np
import sympy as sy

class Superficie(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas, passo=0.1):
        self.linhas = []
        self.passo = passo
        self.coordClip = []
        self.coordenadas = coordenadas
        self.bezier()
        super().__init__(nome, Tipo.SUPERFICIE.value, coordenadas) #ultimo por conta do calc centro
        self.cor = "#034B85"


    @ObjetoGrafico.cor.setter
    def cor(self, valor):
        self._cor = valor
        for obj in self.linhas:
            obj.cor = valor
    
    def normalize(self, mat: np.matrix):
        for obj in self.linhas:
            obj.normalize(mat)

    def projete(self, mat: np.matrix):
        for obj in self.linhas:
            obj.projete(mat)
    
    def calc_centro(self):
        sumX, sumY, sumZ = 0,0,0
        tam = len(self.linhas)
        for i in range(tam):
            sumX += self.linhas[i].centroX
            sumY += self.linhas[i].centroY
            sumZ += self.linhas[i].centroZ
            
        self.centroX = sumX/tam
        self.centroY = sumY/tam
        self.centroZ = sumZ/tam
        self.centro = (self.centroX, self.centroY, self.centroZ)
    
    def moverXY(self, mat: np.matrix, homo=False):
        for obj in self.linhas:
            if homo:
                obj.coordHomo = obj.mulPontoMat3D(mat)
                continue
            obj.coordenadas = obj.mulPontoMat3D(mat)
            obj.calc_centro()
        self.calc_centro()

    def bezier(self):
        self.coordCurv = []
        self.linhas = []
        #t, s = sy.symbols('t s')
        sy.var('t s')

        
        gx = sy.Matrix(
              [[self.coordenadas[0][0],self.coordenadas[1][0],self.coordenadas[2][0],self.coordenadas[3][0]],
              [self.coordenadas[4][0],self.coordenadas[5][0],self.coordenadas[6][0],self.coordenadas[7][0]],
              [self.coordenadas[8][0],self.coordenadas[9][0],self.coordenadas[10][0],self.coordenadas[11][0]],
              [self.coordenadas[12][0],self.coordenadas[13][0],self.coordenadas[14][0],self.coordenadas[15][0]]])
        
        #sy.pprint(gx)
        #print()

        gy = sy.Matrix(
              [[self.coordenadas[0][1],self.coordenadas[1][1],self.coordenadas[2][1],self.coordenadas[3][1]],
              [self.coordenadas[4][1],self.coordenadas[5][1],self.coordenadas[6][1],self.coordenadas[7][1]],
              [self.coordenadas[8][1],self.coordenadas[9][1],self.coordenadas[10][1],self.coordenadas[11][1]],
              [self.coordenadas[12][1],self.coordenadas[13][1],self.coordenadas[14][1],self.coordenadas[15][1]]])
        
        #sy.pprint(gy)
        #print()

        gz = sy.Matrix(
              [[self.coordenadas[0][2],self.coordenadas[1][2],self.coordenadas[2][2],self.coordenadas[3][2]],
              [self.coordenadas[4][2],self.coordenadas[5][2],self.coordenadas[6][2],self.coordenadas[7][2]],
              [self.coordenadas[8][2],self.coordenadas[9][2],self.coordenadas[10][2],self.coordenadas[11][2]],
              [self.coordenadas[12][2],self.coordenadas[13][2],self.coordenadas[14][2],self.coordenadas[15][2]]])

        #sy.pprint(gz)
        #print()

        Tt = sy.Matrix([[t**3], [t**2], [t], [1]])
        S = sy.Matrix([[s**3, s**2, s, 1]])

        Mb = sy.Matrix([[-1,3,-3,1],
                        [3,-6,3,0],
                        [-3,3,0,0],
                        [1,0,0,0]])
        
        SMb = S*Mb
        MbT = Mb*(Tt)  #a transposta de Mb também é Mb


        matx = SMb*gx*MbT
        maty = SMb*gy*MbT
        matz = SMb*gz*MbT
        sAtual = 0
        while sAtual <= 1:              ####################### mudar aqui talvez (Se mudar aqui mudar a linha 120) ####################### 
            x = matx.subs(s, sAtual)
            y = maty.subs(s, sAtual)
            z = matz.subs(s, sAtual)

            self.iteracaot(x, y, z)
            sAtual += self.passo
        
        self.coordCurv = [] #só para não armazenar as várias coordenas por nada

        tAtual = 0
        while tAtual <= 1:              ####################### mudar aqui talvez (Se mudar aqui mudar a linha 109) ####################### 
            x = matx.subs(t, tAtual)
            y = maty.subs(t, tAtual)
            z = matz.subs(t, tAtual)

            self.iteracaos(x, y, z)
            tAtual += self.passo
        
        self.coordCurv = [] #só para não armazenar as várias coordenas por nada


    def iteracaot(self, matx, maty, matz):
        ti = 0
        while ti <= 1:                  ####################### mudar aqui talvez (Se mudar aqui mudar a linha 147) ####################### 
            x = matx.subs(t, ti)
            y = maty.subs(t, ti)
            z = matz.subs(t, ti)
            self.coordCurv.append((x[0,0],y[0,0],z[0,0]))

            if ti != self.passo and ti != 0:
                lin = Line("_", [self.coordCurv[-2], self.coordCurv[-1]])
                self.linhas.append(lin)

            ti += self.passo

    def iteracaos(self, matx, maty, matz):
        si = 0
        while si <= 1:                   ####################### mudar aqui talvez (Se mudar aqui mudar a linha 133)####################### 
            x = matx.subs(s, si)
            y = maty.subs(s, si)
            z = matz.subs(s, si)
            self.coordCurv.append((x[0,0],y[0,0],z[0,0]))
            
            if si != self.passo and si != 0:
                lin = Line("_", [self.coordCurv[-2], self.coordCurv[-1]])
                self.linhas.append(lin)

            si += self.passo


    def superf_clipping(self, clipeLinha):
        for l in self.linhas:
            l.line_clip(clipeLinha)
    
    def mulPontoMat2D(self, mat):
        print("Está chamando mulPontoMat2D para um objeto SUPERFICIE, abortando")
        exit()
    
    def mulPontoMat3D(self, mat):
        print("Está chamando mulPontoMat3D para um objeto SUPERFICIE, abortando")
        exit()
    
    def export(self):
        exp = {}
        exp["nome"] = self.nome 
        coord = []
        for line in self.linhas:
            ponto1 = [line.coordenadas[0][0],line.coordenadas[0][1],line.coordenadas[0][2]]
            ponto2 = [line.coordenadas[1][0],line.coordenadas[1][1],line.coordenadas[1][2]]
            coord.append(ponto1)
            coord.append(ponto2)
        exp["coord"] = coord
        exp["cor"] = self.cor
        exp["tipo"] = self.tipo
       
        return exp