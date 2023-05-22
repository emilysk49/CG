from abstract import ObjetoGrafico, Tipo
from line import Line
import numpy as np
import sympy as sy

class Curve(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas, norm, tipo, passo=0.05):
        self.coordCurv = []
        self.coordClip = []
        self.linhas = []
        self.passo = passo
        self.tipoCurva = tipo
        self.coordenadas = coordenadas
        if self.tipoCurva == "B":
            self.bezier()
        else:               #self.tipo == "s" De spline
            self.spline()
        super().__init__(nome, Tipo.CURVE.value, coordenadas)
        self.cor = "#03BB85"

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

    def moverXY(self, mat: np.matrix, homo=False):
        for obj in self.linhas:
            if homo:
                obj.coordHomo = obj.mulPontoMat3D(mat)
                continue
            obj.coordenadas = obj.mulPontoMat3D(mat)
            obj.calc_centro()
        self.calc_centro()


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

    def bezier(self):
        self.coordCurv = []
        self.linhas = []
        sy.var('t')
        TMb = sy.Matrix([[((-t)**3 +3*t**2 -3*t +1), (3*t**3 -6*t**2 +3*t), (-3*t**3 +3*t**2), t**3]])
        
        for i in range(0,len(self.coordenadas)-1,3):    #de três em três para que o final seja também o inicial da próxima iteração

            gx = sy.Matrix([[self.coordenadas[i][0]],[self.coordenadas[i+1][0]],[self.coordenadas[i+2][0]],[self.coordenadas[i+3][0]]])
            gy = sy.Matrix([[self.coordenadas[i][1]],[self.coordenadas[i+1][1]],[self.coordenadas[i+2][1]],[self.coordenadas[i+3][1]]])
            gz = sy.Matrix([[self.coordenadas[i][2]],[self.coordenadas[i+1][2]],[self.coordenadas[i+2][2]],[self.coordenadas[i+3][2]]])

            TMbGbx = TMb*gx
            TMbGby = TMb*gy
            TMbGbz = TMb*gz
            self.iteracao(TMbGbx, TMbGby, TMbGbz)

    
    def iteracao(self, matx, maty, matz):
        ti = 0
        while ti <= 1:
            x = matx.subs(t, ti)
            y = maty.subs(t, ti)
            z = matz.subs(t, ti)
            self.coordCurv.append((x[0, 0],y[0, 0], z[0, 0]))
            ti += self.passo

            if len(self.coordCurv) > 1:
                lin = Line("_", [self.coordCurv[-2], self.coordCurv[-1]])
                self.linhas.append(lin)


    def spline(self):
        Mbs = sy.Matrix([ [-1/6, 0.5, -0.5, 1/6], [0.5, -1, 0.5, 0], [-0.5, 0, 0.5, 0], [1/6, 2/3, 1/6, 0] ])
        d = self.passo
        E = sy.Matrix([ [0, 0, 0, 1], [d**3, d**2, d, 0], [6*d**3, 2*d**2, 0, 0], [6*d**3, 0, 0, 0] ])
        self.linhas=[]

        for i in range(len(self.coordenadas)-3):
            Gx = sy.Matrix([[self.coordenadas[i][0]], [self.coordenadas[i+1][0]], [self.coordenadas[i+2][0]], [self.coordenadas[i+3][0]]])
            Gy = sy.Matrix([[self.coordenadas[i][1]], [self.coordenadas[i+1][1]], [self.coordenadas[i+2][1]], [self.coordenadas[i+3][1]]])
            Gz = sy.Matrix([[self.coordenadas[i][2]], [self.coordenadas[i+1][2]], [self.coordenadas[i+2][2]], [self.coordenadas[i+3][2]]])

            Cx = Mbs*Gx
            Cy = Mbs*Gy
            Cz = Mbs*Gz

            fx = E*Cx
            fy = E*Cy
            fz = E*Cz

            self.fwdDiff(fx[0,0],fx[1,0],fx[2,0],fx[3,0],fy[0,0],fy[1,0],fy[2,0],fy[3,0],fz[0,0],fz[1,0],fz[2,0],fz[3,0])
        #for passando por todos e gerando Gx e Gy, multiplicando Mbs por elas e ai multiplicar E por esse resultado, ai joga em fwdDiff

    def fwdDiff(self, x, dx, d2x, d3x, y, dy, d2y, d3y, z, dz, d2z, d3z):
        i = 1
        Xvelho = x
        Yvelho = y
        Zvelho = z
        
        n = int(1/self.passo)
        while (i <= n):
            i += 1
            x += dx
            dx += d2x
            d2x += d3x

            y += dy
            dy += d2y
            d2y += d3y

            z += dz
            dz += d2z
            d2z += d3z

            lin = Line("_", [(Xvelho, Yvelho, Zvelho), (x,y,z)])
            lin.coordNorm = [(Xvelho, Yvelho, Zvelho), (x,y,z)]
            self.linhas.append(lin)
           
            Xvelho = x
            Yvelho = y
            Zvelho = z
        
    def curv_clipping(self, clipeLinha):
        for l in self.linhas:
            l.line_clip(clipeLinha)
    
    def export(self, mat: np.matrix):
        exp = {}
        exp["nome"] = self.nome 
        '''
        mat = np.linalg.inv(mat)    #"Desnormalizando" pois nós guardamos as coordCurv já normalizadas para melhor desempenho
        coord = []
        for p in self.coordCurv:
            ponto = [p[0],p[1],p[2]]
            result = np.matmul(ponto, mat)
            coord.append((result.item(0),result.item(1),1))
        '''
        exp["coord"] = self.coordCurv
        exp["cor"] = self.cor
        exp["tipo"] = self.tipo
       
        return exp