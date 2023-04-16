from abstract import ObjetoGrafico, Tipo
from line import Line
import numpy as np
import sympy as sy

class CurveB(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas, norm, passo=0.05):
        super().__init__(nome, Tipo.CURVEB.value, coordenadas)
        self.cor = "#03BB85"
        self.coordCurv = []
        self.coordClip = []
        self.linhas = []
        self.passo = passo
        self.normalize(norm)

    def mulPontoMat(self, mat):
        resposta = []
        for i in self.coordenadas:
            x = i[0]
            y = i[1]
            ponto = [x,y,1]
            result = np.matmul(ponto, mat)
            resposta.append((result.item(0),result.item(1)))
        return resposta

    def moverXY(self, mat):
        self.coordenadas = self.mulPontoMat(mat)
        self.calc_centro()
            
    def normalize(self, mat: np.matrix):
        self.coordNorm = self.mulPontoMat(mat)
        self.bezier()

    def bezier(self):
        self.coordCurv = []
        self.linhas = []
        sy.var('t')
        TMb = sy.Matrix([[((-t)**3 +3*t**2 -3*t +1), (3*t**3 -6*t**2 +3*t), (-3*t**3 +3*t**2), t**3]])
        
        for i in range(0,len(self.coordNorm)-1,3):    #de três em três para que o final seja também o inicial da próxima iteração

            gx = sy.Matrix([[self.coordNorm[i][0]],[self.coordNorm[i+1][0]],[self.coordNorm[i+2][0]],[self.coordNorm[i+3][0]]])
            gy = sy.Matrix([[self.coordNorm[i][1]],[self.coordNorm[i+1][1]],[self.coordNorm[i+2][1]],[self.coordNorm[i+3][1]]])

            TMbGbx = TMb*gx
            TMbGby = TMb*gy
            self.iteracao(TMbGbx, TMbGby)

    
    def iteracao(self, matx, maty):
        ti = 0
        while ti <= 1:
            x = matx.subs(t, ti)
            y = maty.subs(t, ti)
            self.coordCurv.append((x[0, 0],y[0, 0]))
            ti += self.passo

            if len(self.coordCurv) > 1:
                lin = Line("_", [self.coordCurv[-2], self.coordCurv[-1]])
                lin.coordNorm = [self.coordCurv[-2], self.coordCurv[-1]]
                self.linhas.append(lin)

    def export(self):
        print("Inacabada para curvas, pensando em como fazer :)")
        pass