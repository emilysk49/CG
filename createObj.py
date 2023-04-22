from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from point import Point
from line import Line
from polygon import Polygon
from window import Window
from curve import Curve

class CreateObj():
    def __init__(self, window):
        self.w = window

        self.pop = Toplevel(self.w.main_window)
        self.pop.geometry("300x300+450+200")
        self.pop.title("Create New Object")
        self.pop.config(bg="gray")

        #Botoes para selecionar qual objeto adicionar
        Button(self.pop, text="Point", width=5, command=lambda:self.levantar_frame(self.point_frame)).place(x=10, y=10)
        Button(self.pop, text="Line", width=5, command=lambda:self.levantar_frame(self.line_frame)).place(x=10, y=40)
        Button(self.pop, text="Polygon", width=5, command=lambda:self.levantar_frame(self.polygon_frame)).place(x=10, y=70)
        Button(self.pop, text="Curva", width=5, command=lambda:self.levantar_frame(self.curve_frame, self.p4_frame, self.p_frame)).place(x=10,y=100)

        ############################################## PONTO #########################################################
        self.point_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.point_frame.place(x=100, y=0) 
        Label(self.point_frame, bg="gray", text="Nome :").place(x=5, y=5)
        self.nome_point = Entry(self.point_frame, width=12)
        self.nome_point.place(x=52, y=5)
        Label(self.point_frame, bg="gray", text="X :").place(x=5, y=50)
        self.px = Entry(self.point_frame, width=5)
        self.px.place(x=25, y=50)
        Label(self.point_frame, bg="gray", text="Y :").place(x=100, y=50)
        self.py = Entry(self.point_frame, width=5)
        self.py.place(x=120, y=50)
        Button(self.point_frame, text="CONCLUIR", command=lambda:self.criar_ponto()).place(x=50, y=100)
        self.msg_label = Label(self.point_frame, text="", bg="gray")
        self.msg_label.place(x=10, y=150)

        ############################################### LINHA #########################################################
        self.line_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.line_frame.place(x=100, y=0) 
        Label(self.line_frame, bg="gray", text="Nome :").place(x=2, y=5)
        self.nome_line = Entry(self.line_frame, width=12)
        self.nome_line.place(x=50, y=5)
        Label(self.line_frame, bg="gray", text="X1 :").place(x=2, y=50)
        self.lx1 = Entry(self.line_frame, width=5)
        self.lx1.place(x=30, y=50)
        Label(self.line_frame, bg="gray", text="Y1 :").place(x=97, y=50)
        self.ly1 = Entry(self.line_frame, width=5)
        self.ly1.place(x=125, y=50)
        Label(self.line_frame, bg="gray", text="X2 :").place(x=2, y=80)
        self.lx2 = Entry(self.line_frame, width=5)
        self.lx2.place(x=30, y=80)
        Label(self.line_frame, bg="gray", text="Y2 :").place(x=97, y=80)
        self.ly2 = Entry(self.line_frame, width=5)
        self.ly2.place(x=125, y=80)
        Button(self.line_frame, text="CONCLUIR", command=lambda:self.criar_linha()).place(x=50, y=150)
        self.msg_label2 = Label(self.line_frame, text="", bg="gray")
        self.msg_label2.place(x=10, y=180)

        ############################################## POLIGONO #########################################################
        self.polygon_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.polygon_frame.place(x=100, y=0) 
        Label(self.polygon_frame, bg="gray", text="Nome :").place(x=5, y=5)
        self.nome_poly = Entry(self.polygon_frame, width=12)
        self.nome_poly.place(x=52, y=5)
        Label(self.polygon_frame, bg="gray", text="X :").place(x=5, y=50)
        self.polx = Entry(self.polygon_frame, width=5)
        self.polx.place(x=25, y=50)
        Label(self.polygon_frame, bg="gray", text="Y :").place(x=100, y=50)
        self.poly = Entry(self.polygon_frame, width=5)
        self.poly.place(x=120, y=50)
        Button(self.polygon_frame, text="ADICIONAR", command=lambda:self.add_ponto_pol()).place(x=0, y=100)
        Button(self.polygon_frame, text="CONCLUIR", command=lambda:self.criar_poligono()).place(x=100, y=100)
        self.msg_label3 = Label(self.polygon_frame, text="", bg="gray")
        self.msg_label3.place(x=10, y=150)

        ############################################## CURVA #########################################################
        self.curve_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.curve_frame.place(x=100, y=0)

        self.nbC = ttk.Notebook(self.curve_frame)
        self.nbC.place(x=0, y=0, width=200, height=300)


        self.cb = Frame(self.nbC)
        self.cs = Frame(self.nbC)
        self.nbC.add(self.cb, text="Bezier")
        self.nbC.add(self.cs, text="B-Spline")

        ################################################# Bezier #################################################
        self.frame_bezier = Frame(self.cb, borderwidth=1, relief="raised", bg="gray")
        self.frame_bezier.place(x=0, y=0, width=200, height=300)

        Label(self.frame_bezier, bg="gray", text="Nome :").place(x=2, y=5)
        self.nome_curve = Entry(self.frame_bezier, width=12)
        self.nome_curve.place(x=50, y=5)
        #ponto 1
        Label(self.frame_bezier, bg="gray", text="X1:").place(x=2, y=50)
        self.cbX1 = Entry(self.frame_bezier, width=5)
        self.cbX1.place(x=30, y=50)
        Label(self.frame_bezier, bg="gray", text="Y1:").place(x=100, y=50)
        self.cbY1 = Entry(self.frame_bezier, width=5)
        self.cbY1.place(x=125, y=50)
        #ponto 2
        Label(self.frame_bezier, bg="gray", text="X2:").place(x=2, y=80)
        self.cbX2 = Entry(self.frame_bezier, width=5)
        self.cbX2.place(x=30, y=80)
        Label(self.frame_bezier, bg="gray", text="Y2:").place(x=100, y=80)
        self.cbY2 = Entry(self.frame_bezier, width=5)
        self.cbY2.place(x=125, y=80)
        #ponto 3
        Label(self.frame_bezier, bg="gray", text="X3:").place(x=2, y=110)
        self.cbX3 = Entry(self.frame_bezier, width=5)
        self.cbX3.place(x=30, y=110)
        Label(self.frame_bezier, bg="gray", text="Y3:").place(x=100, y=110)
        self.cbY3 = Entry(self.frame_bezier, width=5)
        self.cbY3.place(x=125, y=110)
        #ponto 4
        self.empty_frame = Frame(self.frame_bezier, bg="gray", width=200, height=30) #Frame vazio que sera levantado após a primeira inserção de pontos
        self.empty_frame.place(x=0, y=140)
        #frame inicial para 4 pontos de entrada
        self.p4_frame = Frame(self.frame_bezier, bg="gray", width=200, height=30)
        self.p4_frame.place(x=0, y=140)
        Label(self.p4_frame, bg="gray", text="X4:").place(x=2, y=0)
        self.cbX4 = Entry(self.p4_frame, width=5)
        self.cbX4.place(x=30, y=0)
        Label(self.p4_frame, bg="gray", text="Y4:").place(x=100, y=0)
        self.cbY4 = Entry(self.p4_frame, width=5)
        self.cbY4.place(x=125, y=0)
        
        Button(self.frame_bezier, text="ADICIONAR", command=lambda:self.add_pontos_curvB()).place(x=0, y=185)
        Button(self.frame_bezier, text="CONCLUIR", command=lambda:self.criar_curva("B")).place(x=100, y=185)

        self.msg_label4 = Label(self.frame_bezier, text="", bg="gray")
        self.msg_label4.place(x=10, y=215)

        ################################################# Spline #################################################
        self.frame_spline = Frame(self.cs, borderwidth=1, relief="raised", bg="gray")
        self.frame_spline.place(x=0, y=0, width=200, height=300)

        Label(self.frame_spline, bg="gray", text="Nome :").place(x=2, y=5)
        self.nome_obj5 = Entry(self.frame_spline, width=12)
        self.nome_obj5.place(x=50, y=5)
        #ponto 1
        Label(self.frame_spline, bg="gray", text="X1:").place(x=2, y=50)
        self.csX1 = Entry(self.frame_spline, width=5)
        self.csX1.place(x=30, y=50)
        Label(self.frame_spline, bg="gray", text="Y1:").place(x=100, y=50)
        self.csY1 = Entry(self.frame_spline, width=5)
        self.csY1.place(x=125, y=50)
        #ponto 2
        self.empty_frameCS = Frame(self.frame_spline, bg="gray", width=200, height=90) #Frame vazio que sera levantado após a primeira inserção de pontos
        self.empty_frameCS.place(x=0, y=80)
        self.p_frame = Frame(self.frame_spline, bg="gray", width=200, height=90)
        self.p_frame.place(x=0, y=80)
        #frame inicial para 4 pontos de entrada        
        Label(self.p_frame, bg="gray", text="X2:").place(x=2, y=0)
        self.csX2 = Entry(self.p_frame, width=5)
        self.csX2.place(x=30, y=0)
        Label(self.p_frame, bg="gray", text="Y2:").place(x=100, y=0)
        self.csY2 = Entry(self.p_frame, width=5)
        self.csY2.place(x=125, y=0)
        #ponto 3
        Label(self.p_frame, bg="gray", text="X3:").place(x=2, y=30)
        self.csX3 = Entry(self.p_frame, width=5)
        self.csX3.place(x=30, y=30)
        Label(self.p_frame, bg="gray", text="Y3:").place(x=100, y=30)
        self.csY3 = Entry(self.p_frame, width=5)
        self.csY3.place(x=125, y=30)
        #ponto 4
        Label(self.p_frame, bg="gray", text="X4:").place(x=2, y=60)
        self.csX4 = Entry(self.p_frame, width=5)
        self.csX4.place(x=30, y=60)
        Label(self.p_frame, bg="gray", text="Y4:").place(x=100, y=60)
        self.csY4 = Entry(self.p_frame, width=5)
        self.csY4.place(x=125, y=60)

        
        Button(self.frame_spline, text="ADICIONAR", command=lambda:self.add_pontos_curvS()).place(x=0, y=185)
        Button(self.frame_spline, text="CONCLUIR", command=lambda:self.criar_curva("S")).place(x=100, y=185)

        self.msg_label5 = Label(self.frame_spline, text="", bg="gray")
        self.msg_label5.place(x=10, y=215)

        ############################################## INICIAL #########################################################
        self.pop_padrao = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.pop_padrao.place(x=100, y=0) 
        Label(self.pop_padrao, text="Selecione objeto que \n quer desenhar!", bg="gray").place(x=30, y=120)


    def criar_ponto(self):
        try:
            nome = self.nome_point.get()
            if not (nome in self.w.obj_dict.keys()):         #verifica se nao tem o objeto com mesmo nome 
                x = float(self.px.get())            #cuida que x e y nao recebeu entrada de string
                y = float(self.py.get())
                self.w.object_list.insert(END, nome)         #insere o nome do objeto na listbox
                self.w.obj_dict[nome] = Point(nome, [(x,y)]) #adiciona o ponto no dicionario de objetos, chave = nome
                mat = self.w.gerarDescricaoSCN()             #gera descricao de SCN
                self.w.obj_dict[nome].normalize(mat)         #normaliza objeto criado
                self.w.obj_dict[nome].ponto_clipping()
                self.w.redesenhar()
                self.msg_label.config(text="Ponto adicionado!", foreground="SpringGreen2")
            else:
                self.msg_label.config(text="Nome já existente!", foreground="red")
        except:
            self.msg_label.config(text="Apenas números!", foreground="red")

    def criar_linha(self):
        try:
            nome = self.nome_line.get()
            if not (nome in self.w.obj_dict.keys()):                 #verifica se nao tem o objeto com mesmo nome
                x1 = float(self.lx1.get())                  #cuida se x e y nao recebeu entrada de string
                y1 = float(self.ly1.get())

                x2 = float(self.lx2.get())
                y2 = float(self.ly2.get())
                self.w.object_list.insert(END, nome)                  #insere o nome do objeto na listbox
                self.w.obj_dict[nome] = Line(nome, [(x1,y1),(x2,y2)]) #adiciona a linha no dicionario de objetos, chave = nome
                mat = self.w.gerarDescricaoSCN()                      #gerar descricao de SCN
                self.w.obj_dict[nome].normalize(mat)                  #normaliza objeto criado
                var = self.w.clip_selection.get()
                self.w.obj_dict[nome].line_clip(var)
                self.w.redesenhar()
                self.msg_label2.config(text="Linha adicionada!", foreground="SpringGreen2")
            else:
                self.msg_label2.config(text="Nome já existente!", foreground="red")
        except:
            self.msg_label2.config(text="Apenas números!", foreground="red")

    #enquanto usuario nao concluir, vai adicionado pontos para criacao de poligono
    def add_ponto_pol(self):
        try:
            x = float(self.polx.get()) #cuida que x e y nao recebeu entrada de string
            y = float(self.poly.get())
            self.pontos_pol.append((x,y))
            self.msg_label3.config(text="Ponto adicionado!", foreground="SpringGreen2")
        except:
            self.msg_label3.config(text="Apenas números!", foreground="red")

    #quando usuario concluir adicao de pontos, vai criar poligono
    def criar_poligono(self):
        nome = self.nome_poly.get()
        if not (nome in self.w.obj_dict.keys()):          #verifica se nao tem o objeto com mesmo nome
            self.w.object_list.insert(END, nome)
            pontos = self.pontos_pol[:]                 #copia a lista
            self.w.obj_dict[nome] = Polygon(nome, pontos)
            self.pontos_pol = []
            mat = self.w.gerarDescricaoSCN()              #gerar descricao de SCN
            self.w.obj_dict[nome].normalize(mat)          #normaliza objeto criado
            self.w.obj_dict[nome].weiler_atherton()
            self.w.redesenhar()
            self.msg_label3.config(text="Polígono criado!", foreground="SpringGreen2")
        else:
            self.msg_label3.config(text="Nome já existente!", foreground="red")

    def criar_curva(self, tipo):
        if tipo == "B":
            nome = self.nome_curve.get() #Bezier
            pontos = self.pontos_curvaB[:]
            self.pontos_curvaB = []
        else:
            nome = self.nome_obj5.get() #Spline
            pontos = self.pontos_curvaS[:]
            self.pontos_curvaS = []
        
        if not (nome in self.w.obj_dict.keys()):          #verifica se nao tem o objeto com mesmo nome
            self.w.object_list.insert(END, nome)                
            mat = self.w.gerarDescricaoSCN()              #gerar descricao de SCN
            self.w.obj_dict[nome] = Curve(nome, pontos, mat, tipo)    #curva já tem seus pontos normalizados na criação
            #self.obj_dict[nome].normalize(mat)          #normaliza objeto criado
            self.w.obj_dict[nome].curv_clipping()
            self.w.redesenhar()
            if tipo == "B":
                self.msg_label4.config(text="Curva criada!", foreground="SpringGreen2")
            else:
                self.msg_label5.config(text="Curva criada!", foreground="SpringGreen2")
        else:
            if tipo == "B":
                self.msg_label4.config(text="Nome já existente!", foreground="red")
            else:
                self.msg_label5.config(text="Nome já existente!", foreground="red")

    def add_pontos_curvB(self):
        try:
            adicionar = False
            x1 = float(self.cbX1.get()) #cuida que x e y nao recebeu entrada de string
            y1 = float(self.cbY1.get())
            x2 = float(self.cbX2.get()) #cuida que x e y nao recebeu entrada de string
            y2 = float(self.cbY2.get())
            x3 = float(self.cbX3.get()) #cuida que x e y nao recebeu entrada de string
            y3 = float(self.cbY3.get())
            if not self.pontos_curvaB:
                x4 = float(self.cbX4.get()) #cuida que x e y nao recebeu entrada de string
                y4 = float(self.cbY4.get())
                adicionar = True
            self.pontos_curvaB.append((x1,y1))
            self.pontos_curvaB.append((x2,y2))
            self.pontos_curvaB.append((x3,y3))
            if adicionar:
                self.pontos_curvaB.append((x4,y4))

            self.levantar_frame(self.empty_frame, zerar=False)
            self.msg_label4.config(text="Ponto adicionado!", foreground="SpringGreen2")
        except:
            self.msg_label4.config(text="Apenas números!", foreground="red")

    def add_pontos_curvS(self):
        try:
            adicionar = False
            x1 = float(self.csX1.get()) #cuida que x e y nao recebeu entrada de string
            y1 = float(self.csY1.get())
            if not self.pontos_curvaS:
                x2 = float(self.csX2.get()) 
                y2 = float(self.csY2.get())
                x3 = float(self.csX3.get()) 
                y3 = float(self.csY3.get())
                x4 = float(self.csX4.get()) #cuida que x e y nao recebeu entrada de string
                y4 = float(self.csY4.get())
                adicionar = True
            self.pontos_curvaS.append((x1,y1))
            if adicionar:
                self.pontos_curvaS.append((x2,y2))
                self.pontos_curvaS.append((x3,y3))
                self.pontos_curvaS.append((x4,y4))

            self.levantar_frame(self.empty_frameCS, zerar=False)
            self.msg_label5.config(text="Ponto adicionado!", foreground="SpringGreen2")
        except:
            self.msg_label5.config(text="Apenas números!", foreground="red")

    def apagar_objeto(self):
        #verifica linha onde cursor selecionou
        for linha in self.object_list.curselection():  
            #apaga do dicionario e do list box esse objeto selecionado
            del self.obj_dict[self.object_list.get(linha)] 
            self.object_list.delete(linha)
        self.redesenhar()

    #utilizado para criacao de objetos podendo seleciona varias frames para preencher
    def levantar_frame(self, frame:Frame, frame2:Frame = None, frame3:Frame = None, zerar = True):
        if zerar:
            self.pontos_pol = [] #Ao trocar para outra entrada perde-se o progresso
            self.pontos_curvaS = []
            self.pontos_curvaB = [] 
        frame.tkraise()
        if frame2:
            frame2.tkraise()
        if frame3:
            frame3.tkraise()