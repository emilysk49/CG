from abstract import ObjetoGrafico, Tipo
from line import Line
import numpy as np
import sympy as sy

class Curve(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas, norm, tipo, passo=0.05):
        super().__init__(nome, Tipo.CURVE.value, coordenadas)
        self.cor = "#03BB85"
        self.coordCurv = []
        self.coordClip = []
        self.linhas = []
        self.passo = passo
        self.tipoCurva = tipo
        self.normalize(norm)


    def normalize(self, mat: np.matrix):
        self.coordNorm = self.mulPontoMat2D(mat)
        if self.tipoCurva == "B":
            self.bezier()
        else:               #self.tipo == "s" De spline
            self.spline()

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


    def spline(self):
        Mbs = sy.Matrix([ [-1/6, 0.5, -0.5, 1/6], [0.5, -1, 0.5, 0], [-0.5, 0, 0.5, 0], [1/6, 2/3, 1/6, 0] ])
        d = self.passo
        E = sy.Matrix([ [0, 0, 0, 1], [d**3, d**2, d, 0], [6*d**3, 2*d**2, 0, 0], [6*d**3, 0, 0, 0] ])
        self.linhas=[]

        for i in range(len(self.coordNorm)-3):
            Gx = sy.Matrix([ [self.coordNorm[i][0]], [self.coordNorm[i+1][0]], [self.coordNorm[i+2][0]], [self.coordNorm[i+3][0]]])
            Gy = sy.Matrix([[self.coordNorm[i][1]], [self.coordNorm[i+1][1]], [self.coordNorm[i+2][1]], [self.coordNorm[i+3][1]]])

            Cx = Mbs*Gx
            Cy = Mbs*Gy

            fx = E*Cx
            fy = E*Cy

            self.fwdDiff(fx[0,0],fx[1,0],fx[2,0],fx[3,0],fy[0,0],fy[1,0],fy[2,0],fy[3,0])
        #for passando por todos e gerando Gx e Gy, multiplicando Mbs por elas e ai multiplicar E por esse resultado, ai joga em fwdDiff

    def fwdDiff(self, x, dx, d2x, d3x, y, dy, d2y, d3y):
        i = 1
        Xvelho = x
        Yvelho = y
        
        n = int(1/self.passo)
        while (i <= n):
            i += 1
            x += dx
            dx += d2x
            d2x += d3x

            y += dy
            dy += d2y
            d2y += d3y

            lin = Line("_", [(Xvelho, Yvelho), (x,y)])
            lin.coordNorm = [(Xvelho, Yvelho), (x,y)]
            self.linhas.append(lin)
           
            Xvelho = x
            Yvelho = y
        
    def curv_clipping(self):
        for l in self.linhas:
            l.line_clip("l")
    
    def export(self, mat: np.matrix):
        exp = {}
        exp["nome"] = self.nome 
        mat = np.linalg.inv(mat)
        coord = []
        for p in self.coordCurv:
            ponto = [p[0],p[1],1]
            result = np.matmul(ponto, mat)
            coord.append((result.item(0),result.item(1)))
        exp["coord"] = coord
        exp["cor"] = self.cor
        exp["tipo"] = self.tipo
       
        return exp