from abstract import ObjetoGrafico, Tipo
import numpy as np

class Line(ObjetoGrafico):
    #coordenadas = [()]
    def __init__(self, nome, coordenadas):
        super().__init__(nome, Tipo.LINE.value, coordenadas)
        self.cor = "#0000ff"
        self.desenhavel = bool
        self.coordClip = []

    def moverXY(self, mat):
        self.coordenadas = self.mulPontoMat(mat)

        self.calc_centro()

    def normalize(self, mat: np.matrix):
        self.coordNorm = self.mulPontoMat(mat)


    def liang_barsky(self):
        p = []
        q = []
        
        p.append(-(self.coordNorm[1][0]-self.coordNorm[0][0])) #-delta x
        p.append(self.coordNorm[1][0]-self.coordNorm[0][0])    #delta x
        p.append(-(self.coordNorm[1][1]-self.coordNorm[0][1])) #-delta y
        p.append(self.coordNorm[1][1]-self.coordNorm[0][1])    #delta y

        q.append(self.coordNorm[0][0]-(-1))        #x1-xwmin
        q.append(1-self.coordNorm[0][0])           #xwmax-x1
        q.append(self.coordNorm[0][1]-(-1))        #y1-ywmin
        q.append(1-self.coordNorm[0][1])           #ywmax-y1

        neg = []
        pos = []
        for i in range(len(p)):
            if p[i] < 0:           #se negativo
                neg.append(i)
            elif p[i] > 0:         #se posiivo
                pos.append(i)
            else:                  #se da 0
                if q[i] < 0:       #precisa verificar q[i]
                    self.desenhavel = False
                    return
        
        zeta1 = 0
        for i in neg:
            r = q[i]/p[i]
            zeta1 = max(zeta1,r)

        zeta2 = 1
        for i in pos:
            r= q[i]/p[i]
            zeta2 = min(zeta2, r)

        if zeta1 > zeta2:
            self.desenhavel = False
            return

        if zeta1 != 0:
            x1 = self.coordNorm[0][0] + zeta1*p[1]
            y1 = self.coordNorm[0][1] + zeta1*p[3]
            self.desenhavel = True 
            self.coordClip = [(x1,y1)]
        else:
            x1 = self.coordNorm[0][0]
            y1 = self.coordNorm[0][1]
            self.desenhavel = True
            self.coordClip = [(x1,y1)]
        
        if zeta2 != 1:
            x2 = self.coordNorm[0][0] + zeta2*p[1] #x + zeta2 * delta x
            y2 = self.coordNorm[0][1] + zeta2*p[3] #y + zeta2 * delta y
            self.desenhavel = True
            self.coordClip = [self.coordClip[0], (x2,y2)]
        else:
            x1 = self.coordNorm[1][0]
            y1 = self.coordNorm[1][1]
            self.desenhavel = True
            self.coordClip = [self.coordClip[0], (x1,y1)]
            

    def codigoPonto(self, ponto):
        codigo = 0b00
        if ponto[1] > 1:
            codigo = codigo | 0b10
        elif ponto[1] < -1:
            codigo = codigo | 0b01
        else:
            codigo = codigo | 0b00
        
        codigo = codigo << 2
        if ponto[0] > 1:
            codigo = codigo | 0b10
        elif ponto[0] < -1:
            codigo = codigo | 0b01
        else:
            codigo = codigo | 0b00
        
        return codigo


    def cohen_sutherland(self): #[cima, baixo, direita, esquerda]
        p1 = self.codigoPonto(self.coordNorm[0])
        p2 = self.codigoPonto(self.coordNorm[1])

        if p1 == 0 and p2 == 0:
            self.desenhavel = True
            self.coordClip = self.coordNorm
        elif p1 & p2 != 0:
            self.desenhavel = False
        else:
            clip =[]
            
            if (self.coordNorm[0][0] == self.coordNorm[1][0]):    #No calculo do coeficiente ocorre uma divisão por 0
                for i in range(0,2): #para cada ponto                precisamos tratar a parte
                    if self.coordNorm[i][1] > 1:       # se y passa o topo
                        clip.append((self.coordNorm[i][0], 1))
                    elif self.coordNorm[i][1] < -1:    # se y passa o baixo
                        clip.append((self.coordNorm[i][0], -1))
                    else:
                        clip.append(self.coordNorm[i])
                
                self.desenhavel = True
                self.coordClip = clip
            else:
                p = [p1,p2]                   
                m = ((self.coordNorm[1][1] - self.coordNorm[0][1]) / (self.coordNorm[1][0] - self.coordNorm[0][0]))
                for i in range(2):
                    if p[i] == 0: #está no centro

                        clip.append(self.coordNorm[i])
                        
                    else:
                        var = self.coh_sut_inter(self.coordNorm[i-1], p[i], m)
                        if var == False:
                            self.desenhavel = False
                            return
                        else:
                            clip.append(var)
                
                self.desenhavel = True
                self.coordClip = clip
                
                    


    def coh_sut_inter(self, ponto, reg_code, m):  #m = coeficiente angular
        if reg_code & 0b1000 != 0: #cima 
            x = ponto[0] + (1/m) * (1 - ponto[1])
            if x > -1 and x < 1:
                return (x, 1)
        if reg_code & 0b100 != 0: #baixo
            x = ponto[0] + (1/m) * (-1 - ponto[1])
            if x > -1 and x < 1:
                return (x, -1)

        if reg_code & 0b10 != 0: #direita
            y = m*(1 - ponto[0]) + ponto[1]
            if y > -1 and y < 1:
                return (1, y)
        if reg_code & 0b1 != 0: #esquerda 
            y = m*(-1 - ponto[0]) + ponto[1]
            if y > -1 and y < 1:
              return (-1, y)
        
        return False #caso nao haja interseccao dentro do limite
    
    def line_clip(self, select):
        if (select == "l"):
            self.liang_barsky()
        else: #(var == "c"):
            self.cohen_sutherland()
