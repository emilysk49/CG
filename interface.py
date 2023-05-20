from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.ttk import Style
from point import Point
from line import Line
from polygon import Polygon
from window import Window
from curve import Curve
from arame import Arame
from objHandler import ObjHandler
import numpy as np
from numpy.linalg import norm
import string
from createObj import CreateObj
from PIL import Image, ImageTk

class Interface():
    def __init__(self):
        self.main_window = Tk()
        self.main_window.geometry("930x700+450+200")
        self.main_window.title("Computer Graphic")
        self.main_window["bg"]= "gray"

        style = Style()
        style.theme_use('alt')

        self.obj = ObjHandler()

        self.menubar = Menu(self.main_window)
        self.menubar.option_add("*tearOff", FALSE)
        self.main_window["menu"] = self.menubar
        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label="Menu")
        self.menu_file.add_command(label="Importar", command=self.importar)
        self.menu_file.add_command(label="Exportar", command=self.exportar)

        #relief opcoes: solid, flat, raised, sunken
        #Frame das opcoes escontradas na esquerda da tela
        self.dFile_frame = Frame(self.main_window, borderwidth=1, relief="raised", bg="gray")
        self.dFile_frame.place(x=10, y=10, width=200, height=670)

        #canvas referente a viewport
        self.canvas = Canvas(self.main_window, width=570, height=570, bg="floral white")
        self.canvas.place(x=230, y=10)
        
        self.obj_dict = {}

        #margem para area de clipping
        self.margem = 20 

        #tamanho da tela do viewport (canvas)
        self.xvMin = 0   #0
        self.xvMax = 570 -(self.margem*2) #570 é nosso padrao do canvas,
        self.yvMin = 0   #0                    a margem x2 é para tratar ambos lados
        self.yvMax = 570 -(self.margem*2) #570

        #self.windowObj = Window("Window", [(0.5,2,2.5),(1,0,3),(2.5,2,0.5),(3,0,1)]) #BE BD CD CE

        #self.windowObj = Window("Window", [(0.5,2,2.5),(2.5,2,0.5),(3,0,1),(1,0,3)]) #BE BD CD CE INVERTIDO (olhando a partir do centro)
        #self.windowObj = Window("Window", [(2.5,2,0.5),(0.5,2,2.5),(1,0,3),(3,0,1)]) #NORMAL (olhando como uma pessoa veria)

        #self.windowObj = Window("Window", [(-24.27, 29.27, 22.5), (-29.27, 24.27, 22.5), (-25.73, 20.73, 27.5), (-20.73, 25.73, 27.5)])
        #self.windowObj = Window("Window", [(-11.27, 16.27, 9.5), (-16.27, 11.27, 9.5), (-12.73, 7.73, 14.5), (-7.73, 12.73, 14.5)])

        #self.windowObj = Window("Window", [(2.28,-7.78,-13.28),(13.27,7.77,-2.28),(-2.28,7.78,13.28),(-13.28,-7.78,2.28)]) #BE BD CD CE
        self.windowObj = Window("Window")
        #self.windowObj = Window("Window", [(0,5,0),(5,0,0),(5,0,5),(0,5,5)])
        #self.windowObj = Window("Window", [(5,0,0),(0,5,0),(0,5,5),(5,0,5)])


        self.sup_msg = StringVar(value="Adicione 16 pontos") #Para criar uma superfície e mantermos as mensagens sempre atualizadas

        #ainda nao tem implementacao e apenas frame para logs
        self.log_frame = Frame(self.main_window, borderwidth=1, relief="raised", bg="gray")
        self.log_frame.place(x=230, y=600, width=570, height=80)

        #frame necessario para o scroll
        self.scroll_frame = Frame(self.dFile_frame, bg="black")
        self.scroll_frame.place(x=170, y=20, height=120)
        #Label de texto onde encontramos os objetos
        self.objetos_text = Label(self.dFile_frame, text="Objetos", bg="gray")
        self.objetos_text.config(font =("Courier", 14), foreground="white")
        self.objetos_text.pack()
        self.scrollbar = Scrollbar(self.scroll_frame, orient=VERTICAL)
        #listbox contendo os objetos criados
        self.object_list = Listbox(self.dFile_frame, bg="gray40", yscrollcommand=self.scrollbar.set) 
        #dicionario para que tenhamos uma referencia aos objetos
        self.scrollbar.config(command=self.object_list.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.object_list.place(x=10, y=20, width=155 , height=125)

        #botao para apagar objeto existente
        self.apagarB = Button(self.dFile_frame, text="Delete", command=lambda:self.apagar_objeto())
        self.apagarB.place(x=70, y=155, width=60)
        #botao para adicionar objeto novo -> abre um popup
        self.objectB = Button(self.dFile_frame, text="Add", command=lambda:CreateObj(self))
        self.objectB.place(x=10, y=155, width=60)
        #botao para selecionar cor
        self.colorB = Button(self.dFile_frame, text="Cor", width=2 , command=lambda:self.cor_popup())
        self.colorB.place(x=130, y=155)
        #botao para transformacao
        self.transformarB = Button(self.dFile_frame, text="Transformação", command=lambda:self.transformacao()) #botão para selecionar transformações sobre um objeto
        self.transformarB.place(x=30, y=190)

        #frame das ferramentas de movimento da window
        self.tool_frame = Frame(self.dFile_frame, relief="raised", borderwidth=1, bg="gray")
        self.tool_frame.place(x=10, y=230, width=170, height=420)

        #frame para escolha do clip de linha
        self.choose_frame = Frame(self.tool_frame, relief="raised", borderwidth=1, bg="gray")
        self.choose_frame.place(x=10, y=340, width=150, height=75)


        self.clip_selection = StringVar() #Tipo para receber saida do RadioButton
        #Radiobutton são as partes de click para selecionar opção
        rb = Radiobutton(self.choose_frame, text="Liang Barsky", value="l", variable=self.clip_selection, bg="gray")
        rb.place(x=5,y=0)
        rb2 = Radiobutton(self.choose_frame, text="Cohen Sutherland", value="c", variable=self.clip_selection, bg="gray")
        rb2.place(x=5,y=35)

        #botoes para rotacionar window (padronizamos para 15 graus de rotacao)
        self.esquerda = ImageTk.PhotoImage(Image.open("image/esquerda.png").resize((30,30), Image.ANTIALIAS))
        self.direita = ImageTk.PhotoImage(Image.open("image/direita.png").resize((30,30), Image.ANTIALIAS))
        Button(self.tool_frame, image=self.direita, command=lambda:self.rotacionarWin(15, "z")).place(x=85, y=160)
        Button(self.tool_frame, image=self.esquerda, command=lambda:self.rotacionarWin(-15, "z")).place(x=45, y=160)

        #self.eixos_frame = Frame(self.tool_frame, relief="raised", borderwidth=1, bg="gray")
        #self.eixos_frame.place(x=10, y=250, width=150, height=75)

        self.rotE = ImageTk.PhotoImage(Image.open("image/rotE.png").resize((30,30), Image.ANTIALIAS))
        self.rotD = ImageTk.PhotoImage(Image.open("image/rotD.png").resize((30,30), Image.ANTIALIAS))
        self.rotB = ImageTk.PhotoImage(Image.open("image/rotB.png").resize((30,30), Image.ANTIALIAS))
        self.rotC = ImageTk.PhotoImage(Image.open("image/rotC.png").resize((30,30), Image.ANTIALIAS))

        Button(self.tool_frame, image=self.rotE, command=lambda:self.rotacionarWin(-15, "y")).place(x=45, y=200)
        Button(self.tool_frame, image=self.rotD, command=lambda:self.rotacionarWin(15, "y")).place(x=85, y=200)
        Button(self.tool_frame, image=self.rotB, command=lambda:self.rotacionarWin(15, "x")).place(x=45, y=240)
        Button(self.tool_frame, image=self.rotC, command=lambda:self.rotacionarWin(-15, "x")).place(x=85, y=240)

        Button(self.tool_frame, text="Paralela", command=lambda:self.projecao("para")).place(x=30,y=280)
        Button(self.tool_frame, text="Perspectiva", command=lambda:self.projecao("pers")).place(x=30,y=310)

        #tarefa3 -> agora os eixos tbm sao objetos linhas
        self.eixoX = Line("x", [(-100,0,0), (100,0,0)] )
        self.eixoY = Line("y", [(0,-100,0), (0, 100,0)])
        self.eixoZ = Line("z", [(0,0,-100), (0,0,100)])

        self.pegarEscala() #para poder usar tamanho de window fixo e apenas atualizar no zoomin e zoomout

        self.projetar = "para"
        self.projecao()

        #botoes para navegacao
        self.upB = Button(self.tool_frame, text="UP", width=5, command=lambda:self.up())
        self.upB.place(x=50, y=15)
        self.leftB = Button(self.tool_frame, text="LEFT", width=5, command=lambda:self.left())
        self.leftB.place(x=18, y=45)
        self.rightB = Button(self.tool_frame, text="RIGHT", width=5, command=lambda:self.right())
        self.rightB.place(x=85, y=45)
        self.downB = Button(self.tool_frame, text="DOWN", width=5, command=lambda:self.down())
        self.downB.place(x=50, y=75)

        #botao de zoom in e zoom out
        self.zoominB = Button(self.tool_frame, text="+", width=3, command=lambda:self.zoomIn())
        self.zoominB.place(x=19, y=120)
        self.zoomoutB = Button(self.tool_frame, text="-", width=3, command=lambda:self.zoomOut())
        self.zoomoutB.place(x=100, y=120)

    #transformada de viewport x
    def xvp(self, xw):
        return ( ((xw-(-1))/(1-(-1)))*(self.xvMax-self.xvMin) + self.margem) #padronizando em SCN 
        

    #transformada de viewport y
    def yvp(self, yw):
        return ( (1-((yw-(-1))/(1-(-1))))*(self.yvMax-self.yvMin) + self.margem)  #padronizando em SCN 
    
    #para esquerda <- diminui os x's
    def left(self):
        self.move((-1,0,0))
        

    #para direita -> aumenta os x's
    def right(self):
        #movimenta para direita na visao do usuario
        self.move((1,0,0))

    #para cima ↑ aumenta os y's
    def up(self):
        #movimenta para cima na visao do usuario
        self.move((0,1,0))

    #para baixo ↓ diminui os y's
    def down(self):
        #movimenta para baixo na visao do usuario
        self.move((0,-1,0))

    #zoomin -> aproxima os pontos da window
    def zoomIn(self):
        #zoomin: escalonando para diminuir a tela do window
        mat1 = self.alinhar_eixoZ(False, True)
        self.windowObj.moverXY(mat1)
        mat2 = [[0.9, 0, 0, 0],[0, 0.9, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]]
        mat3 = np.linalg.inv(mat1)
        res = np.matmul(mat2,mat3)

        self.windowObj.escalaX *= 0.9
        self.windowObj.escalaY *= 0.9
        
        self.windowObj.moverXY(res)
        self.projecao()

    
    #zoomout -> afasta os pontos da window
    def zoomOut(self):
        #zoomout: escalonando para aumentar a tela do window
        mat1 = self.alinhar_eixoZ(False, True)

        self.windowObj.moverXY(mat1)
        mat2 = [[1.1, 0, 0, 0],[0, 1.1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]]
        mat3 = np.linalg.inv(mat1)
        res = np.matmul(mat2,mat3)

        self.windowObj.escalaX *= 1.1
        self.windowObj.escalaY *= 1.1

        self.windowObj.moverXY(res)
        self.projecao()
 



    def rotacionarWin(self, ang, sentido):
        #atualiza o angulo do window para rotacionar
        
        mat1 = self.alinhar_eixoZ(False, True)  #segundo argumento trata de receber uma matriz com a normal realmente dentro do eixo Z
        #self.windowObj.moverXY(mat1)            #caso não setarmos como True, alinhar_eixoZ vai realizar uma destranslação e devolver a matriz deslocada (apenas no plano xy)
        mat2 = self.rotacionar3D(ang, sentido)      #mas não com sua normal dentro do eixo Z
        mat3 = np.linalg.inv(mat1)
        res = np.matmul(mat1, mat2)
        res = np.matmul(res,mat3)
        self.windowObj.moverXY(res)
        self.projecao()
        
    

    
    def move(self, tup):
        mat1 = self.alinhar_eixoZ(False)
        self.windowObj.moverXY(mat1)
        mat2 = self.rotacionar3D(self.windowObj.angulo, "z")   #se nao der certo tirar o - e ver...
        mat3 = self.transladar3D(tup[0],tup[1],tup[2])
        res = np.matmul(mat2,mat3)
        mat4 = self.rotacionar3D(-self.windowObj.angulo, "z")
        res = np.matmul(res,mat4)
        mat5 = np.linalg.inv(mat1)
        res = np.matmul(res,mat5)
        self.windowObj.moverXY(res)

        self.projecao()


    def redesenhar(self):
        self.canvas.delete("all") #primeiro apaga tudo

        #redesenha os eixos 
        self.canvas.create_line(self.xvp(self.eixoX.coordNorm[0][0]), self.yvp(self.eixoX.coordNorm[0][1]), self.xvp(self.eixoX.coordNorm[1][0]), self.yvp(self.eixoX.coordNorm[1][1]), fill="red", width=3)
        self.canvas.create_line(self.xvp(self.eixoY.coordNorm[0][0]), self.yvp(self.eixoY.coordNorm[0][1]), self.xvp(self.eixoY.coordNorm[1][0]), self.yvp(self.eixoY.coordNorm[1][1]), fill="green", width=3)
        self.canvas.create_line(self.xvp(self.eixoZ.coordNorm[0][0]), self.yvp(self.eixoZ.coordNorm[0][1]), self.xvp(self.eixoZ.coordNorm[1][0]), self.yvp(self.eixoZ.coordNorm[1][1]), fill="blue", width=3)

        #Desenha a zona do canvas
        self.canvas.create_line(self.xvMin+self.margem, self.yvMin+self.margem ,self.xvMax+self.margem, self.yvMin+self.margem, fill="red", width=3) #Horizontal cima
        self.canvas.create_line(self.xvMax+self.margem, self.yvMin+self.margem, self.xvMax+self.margem, self.yvMax+self.margem, fill="red", width=3) #Vertical direita
        self.canvas.create_line(self.xvMin+self.margem, self.yvMax+self.margem, self.xvMax+self.margem, self.yvMax+self.margem, fill="red", width=3) #Horizontal baixo
        self.canvas.create_line(self.xvMin+self.margem, self.yvMin+self.margem, self.xvMin+self.margem, self.yvMax+self.margem, fill="red", width=3)

        #vai verificar se tem objeto para redesenhar
        for obj in self.obj_dict.values():
            if obj.tipo == 6: #se arame
                for o in obj.obj_list:
                    self.desenhar(o)
            else:
                self.desenhar(obj)
    
    def desenhar(self, obj):
        tup = obj.coordNorm
            
        if obj.tipo == 1: #se ponto
            if obj.desenhavel:
                self.canvas.create_oval(self.xvp(tup[0][0])-3, self.yvp(tup[0][1])-3, self.xvp(tup[0][0])+3, self.yvp(tup[0][1])+3, fill=obj.cor)

        elif obj.tipo == 2: #se linha
            if obj.desenhavel:
                tup = obj.coordClip
                self.canvas.create_line(self.xvp(tup[0][0]), self.yvp(tup[0][1]), self.xvp(tup[1][0]), self.yvp(tup[1][1]), fill=obj.cor, width=3)

        elif obj.tipo == 3: #se poligono
            tup = obj.coordClip
            for i in range (len(tup)-1):
                if tup[i] and tup[i+1] and not(tup[i][1] == "s" and tup[i+1][1] == "e"):     #Utilizamos uma tupla vazia para indicar a parte onde nao queremos traçar uma linha
                                                                                                #Segundo argumento verifica se são duas intersecçoes seguidas, caso sim
                                                                                                #Se for, atenção ao caso de uma saida e uma entrada seguida, ao isso acontecer não trace entre
                    self.canvas.create_line(self.xvp(tup[i][0][0]), self.yvp(tup[i][0][1]), self.xvp(tup[i+1][0][0]), self.yvp(tup[i+1][0][1]), fill=obj.cor, width=3)
        
        elif obj.tipo == 5 or obj.tipo == 7 or obj.tipo == 8: #se curva ou se superficie
            #print("ACHOU UMA CURVA")
            for lin in obj.linhas:
                if lin.desenhavel:
                    tup = lin.coordClip
                    self.canvas.create_line(self.xvp(tup[0][0]), self.yvp(tup[0][1]), self.xvp(tup[1][0]), self.yvp(tup[1][1]), fill=obj.cor, width=3)
        


    def apagar_objeto(self):
        #verifica linha onde cursor selecionou
        for linha in self.object_list.curselection():  
            #apaga do dicionario e do list box esse objeto selecionado
            del self.obj_dict[self.object_list.get(linha)] 
            self.object_list.delete(linha)
        self.redesenhar()


    def transformacao(self): #trata as transformações dos objetos
        if len(self.object_list.curselection()) == 1: #Apenas um objeto selecionado
            self.pop = Toplevel(self.main_window) #Nova janela
            self.pop.geometry("550x400+450+200")
            self.pop.title("Transformações 2D")
            self.pop.config(bg="gray")

            self.obj_trans = self.object_list.get(self.object_list.curselection()) #Nome do objeto selecionado na listbox

            self.nb = ttk.Notebook(self.pop)
            self.nb.place(x=20, y=20, width=350, height=350)

            self.historico_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=150, height=350)
            self.historico_frame.place(x=380, y=20)
            self.scroll2_frame = Frame(self.historico_frame, bg="black")
            self.scroll2_frame.place(x=125, y=10, height=300)
            self.scrollbar2 = Scrollbar(self.scroll2_frame, orient=VERTICAL)
            self.historico = Listbox(self.historico_frame, bg="gray40", yscrollcommand=self.scrollbar2.set) #, yscrollcommand=self.scrollbar2.set
            self.scrollbar2.config(command=self.historico.yview)
            self.scrollbar2.pack(side=RIGHT, fill=Y)
            self.historico.place(x=10, y=10, width=100 , height=300)
            
            self.tb1=Frame(self.nb, relief="raised")    # 3 janelas das tranformações
            self.tb2=Frame(self.nb, relief="raised")
            self.tb3=Frame(self.nb)
            self.nb.add(self.tb1,text="Translação")
            self.nb.add(self.tb2,text="Escalonamento")
            self.nb.add(self.tb3,text="Rotação")

        
            Button(self.historico_frame, text="Adicionar", width=5, command=lambda:self.transformar(self.nb.tab(self.nb.select(), "text"))).place(x=3, y=315)
            Button(self.historico_frame, text="OK", command=lambda:self.fim_trans()).place(x=90, y=315)

            ################### Tab1 (Translação) ###################
            self.ftb1 = Frame(self.tb1, borderwidth=1, relief="raised", bg="gray")
            self.ftb1.place(x=7, y=5, width=330, height=300)

            Label(self.ftb1, bg="gray", text="Transladar por:").place(x=5, y=5)

            Label(self.ftb1, bg="gray", text="DX:").place(x=10, y=50)
            self.entrada_dx = Entry(self.ftb1, width=5)
            self.entrada_dx.place(x=35, y=50)
            
            Label(self.ftb1, bg="gray", text="DY:").place(x=100, y=50)
            self.entrada_dy = Entry(self.ftb1, width=5)
            self.entrada_dy.place(x=125, y=50)

            Label(self.ftb1, bg="gray", text="DZ:").place(x=190, y=50)
            self.entrada_dz = Entry(self.ftb1, width=5)
            self.entrada_dz.place(x=215, y=50)

            self.trans_msg = Label(self.ftb1, text="", bg="gray")
            self.trans_msg.place(x=10, y=100)


            ################### Tab2 (Escalonamento) ###################
            self.ftb2 = Frame(self.tb2, borderwidth=1, relief="raised", bg="gray")
            self.ftb2.place(x=7, y=5, width=330, height=300)

            Label(self.ftb2, bg="gray", text="Escalonar por:").place(x=5, y=5)

            Label(self.tb2, bg="gray", text="SX:").place(x=10, y=50)
            self.entrada_sx = Entry(self.tb2, width=5)
            self.entrada_sx.place(x=35, y=50)
            
            Label(self.tb2, bg="gray", text="SY:").place(x=100, y=50)
            self.entrada_sy = Entry(self.tb2, width=5)
            self.entrada_sy.place(x=125, y=50)

            Label(self.tb2, bg="gray", text="SZ:").place(x=190, y=50)
            self.entrada_sz = Entry(self.tb2, width=5)
            self.entrada_sz.place(x=215, y=50)

            self.scale_msg = Label(self.ftb2, text="", bg="gray")
            self.scale_msg.place(x=10, y=100)


            ################### Tab3 (Rotação) ###################
            self.ftb3 = Frame(self.tb3, borderwidth=1, relief="raised", bg="gray")
            self.ftb3.place(x=7, y=5, width=330, height=300)

            self.select = Frame(self.ftb3, borderwidth=1, relief="raised", bg="gray")
            self.select.place(x=10, y=5, width=310, height=170)

            Label(self.select, bg="gray", text="Opções:").place(x=5, y=5)

            self.option = StringVar()   #Tipo necessário para auxiliar a retirada da opção do Radiobutton

            
            Label(self.ftb3, bg="gray", text="Ângulo:").place(x=20, y=190)
            self.entrada_grau = Entry(self.ftb3, width=5)
            self.entrada_grau.place(x=72, y=190)
            Label(self.ftb3, bg="gray", text="°").place(x=130, y=190)


            self.fr_point = Frame(self.ftb3, borderwidth=1, relief="raised", bg="gray")
            self.fr_point.place(x=10, y=230, width=310, height=60)

            self.fr_general = Frame(self.ftb3, bg="gray")
            self.fr_general.place(x=10, y=230, width=310 , height=60)

            self.general_msg = Label(self.fr_general, text="", bg="gray")
            self.general_msg.place(x=10, y=10)
            
            Label(self.fr_point, bg="gray", text="X:").place(x=10, y=10)
            self.entrada_xp = Entry(self.fr_point, width=5)
            self.entrada_xp.place(x=35, y=10)
 
            Label(self.fr_point, bg="gray", text="Y:").place(x=110, y=10)
            self.entrada_yp = Entry(self.fr_point, width=5)
            self.entrada_yp.place(x=135, y=10)

            Label(self.fr_point, bg="gray", text="Z:").place(x=210, y=10)
            self.entrada_zp = Entry(self.fr_point, width=5)
            self.entrada_zp.place(x=235, y=10)

            self.point_msg = Label(self.fr_point, text="", bg="gray")
            self.point_msg.place(x=10, y=50)

            
            #Radiobutton são as partes de click para selecionar opção
            rb = Radiobutton(self.select, text="Rotacionar sobre eixo x", value="x", variable=self.option, bg="gray", command=lambda:self.levantar_frame(self.fr_general))
            rb.place(x=5,y=35)
            rb2 = Radiobutton(self.select, text="Rotacionar sobre eixo y", value="y", variable=self.option, bg="gray",  command=lambda:self.levantar_frame(self.fr_general))
            rb2.place(x=5,y=65)
            rb3 = Radiobutton(self.select, text="Rotacionar sobre eixo z", value="z", variable=self.option, bg="gray",  command=lambda:self.levantar_frame(self.fr_general))
            rb3.place(x=5,y=95)
            rb4 = Radiobutton(self.select, text="Rotacionar sobre ponto arbitrário", value="a", variable=self.option, bg="gray",  command=lambda:self.levantar_frame(self.fr_point))
            rb4.place(x=5,y=125)
         

    #utilizado para criacao de objetos podendo seleciona varias frames para preencher
    def levantar_frame(self, frame:Frame, frame2:Frame = None, frame3:Frame = None, zerar = True):
        if zerar:
            self.pontos_pol = [] #Ao trocar para outra entrada perde-se o progresso
            self.pontos_curvaS = []
            self.pontos_curvaB = []
            self.pontos_sup = []
            self.sup_msg.set("Adicione 16 pontos!")
        frame.tkraise()
        if frame2:
            frame2.tkraise()
        if frame3:
            frame3.tkraise()

    def transformar(self, tab):
        if tab == "Translação":
            try:
                dx = float(self.entrada_dx.get())   #translação em relação ao eixo X
                dy = float(self.entrada_dy.get())   #translação em relação ao eixo Y
                dz = float(self.entrada_dz.get())
                self.historico.insert(END, f"t {dx} {dy} {dz}")  #insersão na listbox de transformações
                self.trans_msg.config(text="Translação adicionada ao histórico", foreground="SpringGreen2")
            except:
                self.trans_msg.config(text="Números Inválidos", foreground="Red")
                
        elif tab == "Escalonamento":
            try:
                sx = float(self.entrada_sx.get())   #Escalonamento para o ponto no eixo X
                sy = float(self.entrada_sy.get())   #Escalonamento para o ponto no eixo Y
                sz = float(self.entrada_sz.get())
                self.historico.insert(END, f"e {sx} {sy} {sz}")
                self.scale_msg.config(text="Escalonamento adicionado ao histórico", foreground="SpringGreen2")
            except:
                self.scale_msg.config(text="Números Inválidos", foreground="Red")

        elif tab == "Rotação":
            try:
                var = self.option.get()
                angulo = float(self.entrada_grau.get())
                if var == "a": #Rotação sobre um eixo arbitrario
                    x = float(self.entrada_xp.get())
                    y = float(self.entrada_yp.get())
                    z = float(self.entrada_zp.get())
                    self.historico.insert(END, f"ra {x} {y} {z} {angulo}")
                    self.point_msg.config(text="Rotação adicionada ao histórico", foreground="SpringGreen2")

                elif var == "x":    #Rotação sobre o eixo X
                    self.historico.insert(END, f"rx {angulo}")
                    self.general_msg.config(text="Rotação adicionada ao histórico", foreground="SpringGreen2")

                elif var == "y":    #Rotação sobre o eixo Y
                    self.historico.insert(END, f"ry {angulo}")
                    self.general_msg.config(text="Rotação adicionada ao histórico", foreground="SpringGreen2")
                
                elif var == "z":    #Rotação sobre o eixo Z
                    self.historico.insert(END, f"rz {angulo}")
                    self.general_msg.config(text="Rotação adicionada ao histórico", foreground="SpringGreen2")

                else:
                    self.general_msg.config(text="Selecione uma opção de rotação", foreground= "Red")
            except:
                self.general_msg.config(text="Valores Inválidos", foreground="Red")
                self.point_msg.config(text="Valores Inválidos", foreground="Red")
        else: 
            print("Erro a tab veio de forma errada")
    

    def calcular_mat(self):
        historico = self.historico.get(0,END)   #Recebe a listbox com as transformações ordenadas
        ant = np.matrix([[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])    #Matriz identidade (valor simbolico de 1 na mult)
        objName = self.obj_trans    #Nome do objeto
        
        for items in historico:
            lista = items.split()
            match lista[0]:
                case "t": #Translacao
                    dx = float(lista[1])
                    dy = float(lista[2])
                    dz = float(lista[3])
                    mat = self.transladar3D(dx,dy,dz)
                    ant = np.matmul(ant,mat)    #Evolução da matriz de transformações
    
                case "e": #Escalonamento
                    sx = float(lista[1])    #Escalonamento por utilizar a relação do centro do objeto acaba aplicando a matriz de transformação
                    sy = float(lista[2])    # antes, nela é recalculado o centro do objeto, para dai então ser aplicado o escalonamento
                    sz = float(lista[3])
                    self.obj_dict[self.obj_trans].moverXY(ant)
                    ant = np.matrix([[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]])

                    centrox = self.obj_dict[objName].centroX    #Novo centro do objeto X
                    centroy = self.obj_dict[objName].centroY    #Novo centro do objeto Y
                    centroz = self.obj_dict[objName].centroZ    #Novo centro do objeto Z

                    mat1 = self.transladar3D(-centrox, -centroy, -centroz)  #Leva o centro do objeto para a origem das coordenadas
                    ant = np.matmul(ant,mat1)
                    mat2 = self.escalonar3D(sx,sy,sz)                #Escalona a matriz em relação a Sx e Sy
                    ant = np.matmul(ant,mat2)
                    mat3 = self.transladar3D(centrox, centroy, centroz)    #Devolve o centro do objeto até a posição original
                    ant = np.matmul(ant,mat3)

                case "rx": #Rotacao sobre eixo X
                    ang = float(lista[1])
                    mat = self.rotacionar3D(ang, "x")                  #Simplesmente rotaciona em relação a origem
                    ant = np.matmul(ant,mat)
                
                case "ry": #Rotacao sobre eixo Y
                    ang = float(lista[1])
                    mat = self.rotacionar3D(ang, "y")                  #Simplesmente rotaciona em relação a origem
                    ant = np.matmul(ant,mat)

                case "rz": #Rotacao sobre eixo Z
                    ang = float(lista[1])
                    mat = self.rotacionar3D(ang, "z")                  #Simplesmente rotaciona em relação a origem
                    ant = np.matmul(ant,mat)

                case "ra": #Rotação por um eixo arbitrario (que passa pelo centro do obj)
                    px = float(lista[1])
                    py = float(lista[2])
                    pz = float(lista[3])
                    ang = float(lista[4])

                    mat1 = self.transladar3D(-px, -py, -pz)                #Leva o ponto para a origem das coordenadas
                    ant = np.matmul(ant,mat1)
                    
                    centrox = self.obj_dict[objName].centroX
                    centroy = self.obj_dict[objName].centroY
                    centroz = self.obj_dict[objName].centroZ

                    vetorA = [centrox-px, centroy-py, centroz-pz]

                    tanx = vetorA[1]/vetorA[2] #y/z
                    tany = vetorA[0]/vetorA[2] #x/z

                    anguloX = np.degrees(np.arctan(tanx))
                    anguloY = np.degrees(np.arctan(tany))

                    mat2 = self.rotacionar3D(anguloX, "x")      #Fazemos o vetor ser paralelo ao plano x, y
                    mat3 = self.rotacionar3D(anguloY, "y")      #Colocamos o vetor paralelo ao eixo z
                    
                    ant = np.matmul(ant,mat2)
                    ant = np.matmul(ant,mat3)

                    mat4 = self.rotacionar3D(ang, "z")          #Rotaciona o objeto pelo ângulo dado
                    ant = np.matmul(ant,mat4)

                    mat5 = self.rotacionar3D(-anguloX, "x")      #Desfazemos as rotações anteriores
                    mat6 = self.rotacionar3D(-anguloY, "y")
                    
                    ant = np.matmul(ant,mat5)
                    ant = np.matmul(ant,mat6)
                    
                    mat7 = self.transladar3D(px, py, pz)                  #Devolve o ponto até a posição original
                    ant = np.matmul(ant,mat7)
        return ant

    def transladar3D(self, dx, dy, dz):
        return np.matrix([[1,0,0,0], [0,1,0,0], [0,0,1,0], [dx,dy,dz,1]]) #translação em 3D
    
    def transladar2D(self, dx, dy):
        return np.matrix([[1,0,0], [0,1,0], [dx,dy,1]])

    def escalonar3D(self, sx, sy, sz):
        return np.matrix([[sx,0,0,0], [0,sy,0,0], [0,0,sz,0], [0,0,0,1]]) #escalonar em 3D
    
    def escalonar2D(self, sx, sy):
        return np.matrix([[sx,0,0], [0,sy,0], [0,0,1]])

    #np.sin(np.deg2rad(90))
    def rotacionar2D(self, ang):                                      #Devolve a matriz da rotação
        return np.matrix([[np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang)),  0], [-np.sin(np.deg2rad(ang)), np.cos(np.deg2rad(ang)), 0], [0,0,1]])

    def rotacionar3D(self, ang, eixo):
        if eixo == "x":
            return np.matrix([[1,0,0,0],[0,np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang)), 0], [0,-np.sin(np.deg2rad(ang)), np.cos(np.deg2rad(ang)), 0], [0,0,0,1]])
        elif eixo == "y":
            return np.matrix([[np.cos(np.deg2rad(ang)),0,-np.sin(np.deg2rad(ang)),0],[0,1,0,0], [np.sin(np.deg2rad(ang)),0, np.cos(np.deg2rad(ang)), 0], [0,0,0,1]])
        else:
            return np.matrix([[np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang)), 0,0], [-np.sin(np.deg2rad(ang)), np.cos(np.deg2rad(ang)), 0,0], [0,0,1,0], [0,0,0,1]])

    def fim_trans(self):
        self.mat = self.calcular_mat()      #Calcula a matriz de transições
        self.historico.delete(0, END)
        obj = self.obj_dict[self.obj_trans]
        obj.moverXY(self.mat) #Proprio objeto aplica a matriz conforme sua especificidade
        obj.moverXY(self.mathomo, True)
        mat = self.gerarDescricaoSCN()
        obj.normalize(mat)
        if (obj.tipo == 1):
            obj.ponto_clipping()
        elif (obj.tipo == 2):
            var = self.clip_selection.get()
            obj.line_clip(var)
        elif (obj.tipo == 3):
            obj.weiler_atherton()
        elif (obj.tipo == 5):
            var = self.clip_selection.get()
            obj.curv_clipping(var)
        elif (obj.tipo == 6):
            var = self.clip_selection.get()
            obj.arame_clipping(var)
        elif (obj.tipo == 7 or obj.tipo == 8):
            var = self.clip_selection.get()
            obj.superf_clipping(var)
        self.redesenhar()

    def cor_popup(self):
        if len(self.object_list.curselection()) == 1:                               #Apenas um objeto selecionado
            self.obj_act = self.object_list.get(self.object_list.curselection())    #Nome do objeto selecionado na listbox
            self.pop = Toplevel(self.main_window)
            self.pop.geometry("400x100+450+200")
            self.pop.title("Cor RGB")
            self.pop.config(bg="gray")

            Label(self.pop, text="Digite cor que gostaria em HEXADECIMAL", bg="gray").place(x=20, y=10)
            Label(self.pop, text="#", bg="gray").place(x=20,y=40)
            rgb = Entry(self.pop, width=20)
            rgb.place(x=40,y=40)
            
            self.msg_rgb = Label(self.pop, text="", bg="gray")
            self.msg_rgb.place(x=40,y=65)

            Button(self.pop, text="Confirmar", command=lambda:self.apply_color(str(rgb.get()))).place(x=250,y=40)
            

    def apply_color(self, rgb):
        rgbmin = rgb.lower()
        if len(rgbmin) != 6:    #Caso mais ou menos do que 6 caracteres na entrada
            self.msg_rgb.configure(text="São 6 números para codificar o RGB!", foreground="red")
            return
        for i in rgbmin: 
            if i not in string.hexdigits: #Caso um caracter não pertença aos hexadecimais
                self.msg_rgb.configure(text="Insira números no formato HEXADECIMAL!", foreground="red")
                return
        self.obj_dict[self.obj_act].cor = "#"+ rgbmin   #Objeto armazena sua cor
        self.msg_rgb.configure(text="Cor alterada com sucesso", foreground="SpringGreen2")
        self.redesenhar()
        
    #############################################################################################################################################################################

    def gerarDescricaoSCN(self):
        #trasladar o centro do window para origem
        #mat1 = self.transladar2D(-self.windowObj.centroXHomo, -self.windowObj.centroYHomo) 
        mat2 = self.rotacionar2D(self.windowObj.angulo)
        #print(f"angulo de window: {self.windowObj.angulo}")

        #escalona para normalizar em SCN [-1,1]
        mat3 = self.escalonar2D(1/(self.windowObj.escalaX/2), 1/(self.windowObj.escalaY/2))
        #print(f"mat3 transladar: {mat3}")
        #result = np.matmul(mat1, mat2)
        result = np.matmul(mat2, mat3)
        return result
        

    def normalizar(self):
        mat = self.gerarDescricaoSCN()

        #aplica normalizacao para todos objetos
        for obj in self.obj_dict.values():
            obj.normalize(mat)
            if (obj.tipo == 1):
                obj.ponto_clipping()
            elif (obj.tipo == 2):
                var = self.clip_selection.get()
                obj.line_clip(var)
            elif (obj.tipo == 3):
                obj.weiler_atherton()
            elif (obj.tipo == 5):
                var = self.clip_selection.get()
                obj.curv_clipping(var)
            elif (obj.tipo == 6):
                var = self.clip_selection.get()
                obj.arame_clipping(var)
            elif (obj.tipo == 7 or obj.tipo == 8):
                var = self.clip_selection.get()
                obj.superf_clipping(var)
        self.eixoY.normalize(mat)
        self.eixoX.normalize(mat)
        self.eixoZ.normalize(mat)

    

    def importar(self):
        var = self.clip_selection.get()
        objetos = self.obj.open_file()

        for o in objetos:
            self.object_list.insert(END, o.nome)         #insere o nome do objeto na listbox
            self.obj_dict[o.nome] = o                    #adiciona o ponto no dicionario de objetos, chave = nome
            #mat = self.gerarDescricaoSCN()               #gera descricao de SCN
            #self.obj_dict[o.nome].normalize(mat)         #normaliza objeto criado
        
            #if (o.tipo == 1):
            #    self.obj_dict[o.nome].ponto_clipping()
            #elif (o.tipo == 2):
            #    self.obj_dict[o.nome].line_clip(var)
            #elif (o.tipo == 3):
            #    self.obj_dict[o.nome].weiler_atherton()
            #elif (o.tipo == 5):
            #    self.obj_dict[o.nome].line_clip(var)
        #print("Terminando importar")
        self.projecao()
        #self.redesenhar()

    def exportar(self):
        list_obj = []
        for obj in self.obj_dict.values():
            if obj.tipo == 5:
                mat = self.gerarDescricaoSCN()
                list_obj.append(obj.export(mat))
            elif obj.tipo == 6:
                for object in obj.obj_list:
                    if object.tipo == 5:
                        mat = self.gerarDescricaoSCN()
                        list_obj.append(object.export(mat))
                    else:
                        list_obj.append(object.export()) 
            else:
                list_obj.append(obj.export())               #Cada objeto prepara uma dicionário próprio
        self.obj.write_file(list_obj)                   #para auxiliar na exportação


    def pegarEscala(self):
        mat1 = self.alinhar_eixoZ(False, True)
        self.windowObj.moverXY(mat1)
        mat2 = self.rotacionar3D(-self.windowObj.angulo, "z")   #se nao der certo tirar o - e ver.
        self.windowObj.moverXY(mat2)
        self.windowObj.escalaX = abs(self.windowObj.coordenadas[1][0]- self.windowObj.coordenadas[0][0]) #BD - BE (x)
        self.windowObj.escalaY = abs(self.windowObj.coordenadas[3][1]- self.windowObj.coordenadas[0][1]) #CE - BE (y)
        mat3 = self.rotacionar3D(self.windowObj.angulo, "z")
        mat4 = np.linalg.inv(mat1)
        res = np.matmul(mat3,mat4)
        self.windowObj.moverXY(res)
        #print(f"Escala X inicial: {self.windowObj.escalaX}")
        #print(f"Escala Y inicial: {self.windowObj.escalaY}")

    def projecao(self, alt=""):
        if alt:
            self.projetar = alt
        
        if self.projetar == "para":
            self.projParalela()
        else:
            self.projPerspectiva()
            
    
    def projPerspectiva(self, d=1): #padronizando 3 unidade para tras
        """
        2. Determine os ângulos de VPN com X e Y
        3. Rotacione o mundo em torno de X e Y de forma a alinhar VPN com o eixo Z
        1. Translade COP para a origem
        4. Projete, calculando x e y usando 6.2.
        5. Normalize x e y (coordenadas de window)
        6. Clippe 2D
        7. Transforme para coordenadas de Viewport
        """
        mat = self.transladar3D(0,0,d) 
        mat = np.matmul(self.alinhar_eixoZ(True), mat)

        #mat4 = [[1,0,0,0],[0,1,0,0], [0,0,1,0], [0,0,1/d,0]]
        mat4 = [[1,0,0,0],[0,1,0,0], [0,0,1,1/d], [0,0,0,0]]
        
        
        self.mathomo = np.matmul(mat, mat4)
        self.windowObj.moverXY(self.mathomo, True)
        self.windowObj.calc_angulo()

        for obj in self.obj_dict.values():
            obj.moverXY(self.mathomo, True)
            obj.projete(mat4)

        self.eixoX.moverXY(self.mathomo, True) 
        #self.eixoX.projete(mat4)   
        #print(f"eixo x: {self.eixoX.coordHomo}")     
        self.eixoY.moverXY(self.mathomo, True)
        #self.eixoY.projete(mat4) 
        #print(f"eixo y: {self.eixoY.coordHomo}")
        self.eixoZ.moverXY(self.mathomo, True)
        #self.eixoZ.projete(mat4) 
        #print(f"eixo z: {self.eixoZ.coordHomo}")
        
        
        self.normalizar()
        self.redesenhar()

        
    def projParalela(self):
        """
        1.	Translade VRP para a origem
        2.	Determine VPN
                Decomponha e determine os ângulos de VPN com X e Y
        3.	Rotacione o mundo em torno de X e Y de forma a alinhar VPN com o eixo Z
        4.	Ignore todas as coordenadas Z dos objetos.
        5.	Normalize o resto (coordenadas de window)
        6.	Clippe
        7.	Transforme para coordenadas de Viewport 
        """
        
        self.mathomo = self.alinhar_eixoZ(True)
        
        ##########################
        self.windowObj.moverXY(self.mathomo, True)
        self.windowObj.calc_angulo()
        #print(f"window: \n{self.windowObj.coordHomo}")
        for obj in self.obj_dict.values():
            obj.moverXY(self.mathomo, True)

        self.eixoX.moverXY(self.mathomo, True)    
        #print(f"eixo x: {self.eixoX.coordHomo}")     
        self.eixoY.moverXY(self.mathomo, True)
        #print(f"eixo y: {self.eixoY.coordHomo}")
        self.eixoZ.moverXY(self.mathomo, True)
        #print(f"eixo z: {self.eixoZ.coordHomo}")

        self.normalizar()
        self.redesenhar()

    
    def alinhar_eixoZ(self, homo, centro = False):
        x, y, z = self.windowObj.centroX, self.windowObj.centroY, self.windowObj.centroZ
        
        mat1 = self.transladar3D(-x,-y,-z)
        
        vetor1 = []
        vetor2 = []
        for i in range(3):
            vetor1.append( self.windowObj.centro[i] - self.windowObj.CE[i]) #criando vetor 1
            vetor2.append( self.windowObj.CD[i] - self.windowObj.centro[i]) #criando vetor 2


        normal = np.cross(vetor1, vetor2) #produto vetorial

        tanx = normal[1]/normal[2] #y/z

        anguloX = np.degrees(np.arctan(tanx))

        mat2 = self.rotacionar3D(anguloX, "x")
        mat = np.matmul(mat1,mat2)
        self.windowObj.moverXY(mat, True)
        
        #####################################
        vetor1 = []
        vetor2 = []
        
        for i in range(3):
            vetor1.append( self.windowObj.centroHomo[i] - self.windowObj.coordHomo[3][i])
            vetor2.append( self.windowObj.coordHomo[2][i] - self.windowObj.centroHomo[i])
        

        normal = np.cross(vetor1, vetor2) #produto vetorial
        tany = normal[0]/normal[2] #x/z
        anguloY = -np.degrees(np.arctan(tany))

        #print(anguloY)
        mat3 = self.rotacionar3D(anguloY, "y")

        res = np.matmul(mat, mat3)
        if (not homo) and (not centro):        #Devolve para uma posição deslocada
            mat1 = np.linalg.inv(mat1)
            res = np.matmul(res, mat1)
        return res


    