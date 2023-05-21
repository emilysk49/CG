from abstract import ObjetoGrafico, Tipo
from line import Line
import numpy as np
import sympy as sy

class SuperficieB(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas, passo=0.1):
        self.linhas = []
        self.passo = passo
        self.coordSup = []
        self.coordClip = []
        self.coordenadas = sy.Matrix(coordenadas)  #Coordenadas aqui sao a matriz inserida pelo usuario
        self.bSpline()
        super().__init__(nome, Tipo.SUPERFICIEB.value, coordenadas) #ultimo por conta do calc centro
        self.cor = "#A34BA5"

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


    ############################################# Superficie fwd Diff #######################################################

    def bSpline(self):
        """ 1. Calcule os coeficientes:
                Cx = Mmétodo . Gx . MTmétodo Cy = Mmétodo . Gy . MTmétodo Cz = Mmétodo . Gz . MTmétodo
            2. Calcule os deltas para ni passos em t e s: ds = 1/(ns - 1)
                                                          dt = 1/(nt - 1)
        """
        Mbs = sy.Matrix([ [-1/6, 0.5, -0.5, 1/6], [0.5, -1, 0.5, 0], [-0.5, 0, 0.5, 0], [1/6, 2/3, 1/6, 0] ])
        d = self.passo
        E = sy.Matrix([ [0, 0, 0, 1], [d**3, d**2, d, 0], [6*d**3, 2*d**2, 0, 0], [6*d**3, 0, 0, 0] ])
        self.linhas=[]

        for i in range(self.coordenadas.shape[0]-3): #linhas
            for j in range(self.coordenadas.shape[1]-3): #colunas
                
                gx = sy.Matrix([[self.coordenadas[i,j][0],self.coordenadas[i,j+1][0],self.coordenadas[i,j+2][0],self.coordenadas[i,j+3][0]],
                                [self.coordenadas[i+1,j][0],self.coordenadas[i+1,j+1][0],self.coordenadas[i+1,j+2][0],self.coordenadas[i+1,j+3][0]],
                                [self.coordenadas[i+2,j][0],self.coordenadas[i+2,j+1][0],self.coordenadas[i+2,j+2][0],self.coordenadas[i+2,j+3][0]],
                                [self.coordenadas[i+3,j][0],self.coordenadas[i+3,j+1][0],self.coordenadas[i+3,j+2][0],self.coordenadas[i+3,j+3][0]]])

                gy = sy.Matrix([[self.coordenadas[i,j][1],self.coordenadas[i,j+1][1],self.coordenadas[i,j+2][1],self.coordenadas[i,j+3][1]],
                                [self.coordenadas[i+1,j][1],self.coordenadas[i+1,j+1][1],self.coordenadas[i+1,j+2][1],self.coordenadas[i+1,j+3][1]],
                                [self.coordenadas[i+2,j][1],self.coordenadas[i+2,j+1][1],self.coordenadas[i+2,j+2][1],self.coordenadas[i+2,j+3][1]],
                                [self.coordenadas[i+3,j][1],self.coordenadas[i+3,j+1][1],self.coordenadas[i+3,j+2][1],self.coordenadas[i+3,j+3][1]]])

                gz = sy.Matrix([[self.coordenadas[i,j][2],self.coordenadas[i,j+1][2],self.coordenadas[i,j+2][2],self.coordenadas[i,j+3][2]],
                                [self.coordenadas[i+1,j][2],self.coordenadas[i+1,j+1][2],self.coordenadas[i+1,j+2][2],self.coordenadas[i+1,j+3][2]],
                                [self.coordenadas[i+2,j][2],self.coordenadas[i+2,j+1][2],self.coordenadas[i+2,j+2][2],self.coordenadas[i+2,j+3][2]],
                                [self.coordenadas[i+3,j][2],self.coordenadas[i+3,j+1][2],self.coordenadas[i+3,j+2][2],self.coordenadas[i+3,j+3][2]]])

                
                cx = Mbs*gx*(Mbs.transpose())
                cy = Mbs*gy*(Mbs.transpose())
                cz = Mbs*gz*(Mbs.transpose())


                self.fwdDiff(cx, cy, cz, E)


    def fwdDiff(self, cx, cy, cz, E):

        ddx = E*cx*E.transpose()
        ddy = E*cy*E.transpose()
        ddz = E*cz*E.transpose()

        ddxcopy = ddx
        ddycopy = ddy
        ddzcopy = ddz

        i = 1
        n = int(1/(self.passo))
        
        while (i <= n):
            self.fwdDiffCurva(ddx[0,0],ddx[0,1],ddx[0,2],ddx[0,3],
                              ddy[0,0],ddy[0,1],ddy[0,2],ddy[0,3],
                              ddz[0,0],ddz[0,1],ddz[0,2],ddz[0,3])
            
            

            # Somar a segunda linha com a primeira linha
            for c in range(3):
                ddx = ddx.elementary_row_op(op="n->n+km", row=c, k=1, row1=c, row2=c+1)
                ddy = ddy.elementary_row_op(op="n->n+km", row=c, k=1, row1=c, row2=c+1)
                ddz = ddz.elementary_row_op(op="n->n+km", row=c, k=1, row1=c, row2=c+1)
                

            i += 1
        
        ddx = ddxcopy.transpose()
        ddy = ddycopy.transpose()
        ddz = ddzcopy.transpose()


        i = 1
        while (i <= n):
            self.fwdDiffCurva(ddx[0,0],ddx[0,1],ddx[0,2],ddx[0,3],
                              ddy[0,0],ddy[0,1],ddy[0,2],ddy[0,3],
                              ddz[0,0],ddz[0,1],ddz[0,2],ddz[0,3])
            
            

            # Somar a segunda linha com a primeira linha
            for c in range(3):
                ddx = ddx.elementary_row_op(op="n->n+km", row=c, k=1, row1=c, row2=c+1) #linha1 = linha1 + linha2
                ddy = ddy.elementary_row_op(op="n->n+km", row=c, k=1, row1=c, row2=c+1) #linha2 = linha2 + linha3
                ddz = ddz.elementary_row_op(op="n->n+km", row=c, k=1, row1=c, row2=c+1) #linha3 = linha3 + linha4
                
            i += 1


    def fwdDiffCurva(self, x, dx, d2x, d3x, y, dy, d2y, d3y, z, dz, d2z, d3z):
        i = 1
        Xvelho = x
        Yvelho = y
        Zvelho = z
        
        #n = 5 #
        n = int(1/self.passo) #tentar melhorar o desempenho
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
            self.linhas.append(lin)
           
            Xvelho = x
            Yvelho = y
            Zvelho = z

    def superf_clipping(self, clipeLinha):
        for l in self.linhas:
            l.line_clip(clipeLinha)

    def export(self, mat: np.matrix):
        exp = {}
        exp["nome"] = self.nome 
        mat = np.linalg.inv(mat)    #"Desnormalizando" pois nós guardamos as coordCurv já normalizadas para melhor desempenho
        coord = []
        for line in self.linhas:
            ponto1 = [line.coordenadas[0][0],line.coordenadas[0][1],line.coordenadas[0][2]]
            ponto2 = [line.coordenadas[1][0],line.coordenadas[1][1],line.coordenadas[0][2]]
            #result1 = np.matmul(ponto1, mat)
            #result2 = np.matmul(ponto2, mat)
            #coord.append((result1.item(0),result1.item(1),1))
            #coord.append((result2.item(0),result2.item(1),1))
            coord.append(ponto1)
            coord.append(ponto2)
        exp["coord"] = coord
        exp["cor"] = self.cor
        exp["tipo"] = self.tipo
       
        return exp