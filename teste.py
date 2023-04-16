from sympy import *
import numpy as np

def bezier():
        var('t')
        TMb = Matrix([[((-t)**3 +3*t**2 -3*t +1), (3*t**3 -6*t**2 +3*t), (-3*t**3 +3*t**2), t**3]])
        coordenadas = [(1,1),(2,3),(3,0),(4,1),(5,2),(4,4),(6,4),(7,4),(6,2),(7,1)]
        for i in range(0,len(coordenadas)-1,3):
            #gx=[]
            gy=[]
            #gx.append([coordenadas[i][0]])
            #gx.append([coordenadas[i+1][0]])
            #gx.append([coordenadas[i+2][0]])
            #gx.append([coordenadas[i+3][0]])

            gx = Matrix([[coordenadas[i][0]],[coordenadas[i+1][0]],[coordenadas[i+2][0]],[coordenadas[i+3][0]]])

            gy.append([coordenadas[i][1]])
            gy.append([coordenadas[i+1][1]])
            gy.append([coordenadas[i+2][1]])
            gy.append([coordenadas[i+3][1]])

            TMbGbx = TMb*gx
            #TMbGby = TMb*gy
            print(TMbGbx)

bezier()