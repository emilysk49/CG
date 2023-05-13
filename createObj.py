from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from point import Point
from line import Line
from polygon import Polygon
from window import Window
from curve import Curve
from arame import Arame
from superficie import Superficie

class CreateObj():
    def __init__(self, window):
        self.w = window

        self.pop = Toplevel(self.w.main_window)
        self.pop.geometry("400x300+450+200")
        self.pop.title("Create New Object")
        self.pop.config(bg="gray")

        #Botoes para selecionar qual objeto adicionar
        Button(self.pop, text="Point", width=5, command=lambda:self.w.levantar_frame(self.point_frame)).place(x=10, y=10)
        Button(self.pop, text="Line", width=5, command=lambda:self.w.levantar_frame(self.line_frame)).place(x=10, y=40)
        Button(self.pop, text="Polygon", width=5, command=lambda:self.w.levantar_frame(self.polygon_frame)).place(x=10, y=70)
        Button(self.pop, text="Curva", width=5, command=lambda:self.w.levantar_frame(self.curve_frame, self.p4_frame, self.p_frame)).place(x=10,y=100)
        Button(self.pop, text="Arame", width=5, command=lambda:self.w.levantar_frame(self.arame_frame)).place(x=10,y=130)
        Button(self.pop, text="Superficie", width=5, command=lambda:self.w.levantar_frame(self.superf_frame)).place(x=10,y=160)

        ############################################## PONTO #########################################################
        self.point_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=300, height=300)
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
        Label(self.point_frame, bg="gray", text="Z :").place(x=195, y=50)
        self.pz = Entry(self.point_frame, width=5)
        self.pz.place(x=215, y=50)
        Button(self.point_frame, text="CONCLUIR", command=lambda:self.criar_ponto()).place(x=50, y=100)
        self.msg_label = Label(self.point_frame, text="", bg="gray")
        self.msg_label.place(x=10, y=150)

        ############################################### LINHA #########################################################
        self.line_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=300, height=300)
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
        Label(self.line_frame, bg="gray", text="Z1 :").place(x=192, y=50)
        self.lz1 = Entry(self.line_frame, width=5)
        self.lz1.place(x=220, y=50)
        Label(self.line_frame, bg="gray", text="X2 :").place(x=2, y=80)
        self.lx2 = Entry(self.line_frame, width=5)
        self.lx2.place(x=30, y=80)
        Label(self.line_frame, bg="gray", text="Y2 :").place(x=97, y=80)
        self.ly2 = Entry(self.line_frame, width=5)
        self.ly2.place(x=125, y=80)
        Label(self.line_frame, bg="gray", text="Z2 :").place(x=192, y=80)
        self.lz2 = Entry(self.line_frame, width=5)
        self.lz2.place(x=220, y=80)
        Button(self.line_frame, text="CONCLUIR", command=lambda:self.criar_linha()).place(x=50, y=150)
        self.msg_label2 = Label(self.line_frame, text="", bg="gray")
        self.msg_label2.place(x=10, y=180)

        ############################################## POLIGONO #########################################################
        self.polygon_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=300, height=300)
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
        Label(self.polygon_frame, bg="gray", text="Z :").place(x=195, y=50)
        self.polz = Entry(self.polygon_frame, width=5)
        self.polz.place(x=215, y=50)
        Button(self.polygon_frame, text="ADICIONAR", command=lambda:self.add_ponto_pol()).place(x=0, y=100)
        Button(self.polygon_frame, text="CONCLUIR", command=lambda:self.criar_poligono()).place(x=100, y=100)
        self.msg_label3 = Label(self.polygon_frame, text="", bg="gray")
        self.msg_label3.place(x=10, y=150)

        ############################################## CURVA #########################################################
        self.curve_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=300, height=300)
        self.curve_frame.place(x=100, y=0)

        self.nbC = ttk.Notebook(self.curve_frame)
        self.nbC.place(x=0, y=0, width=300, height=300)


        self.cb = Frame(self.nbC)
        self.cs = Frame(self.nbC)
        self.nbC.add(self.cb, text="Bezier")
        self.nbC.add(self.cs, text="B-Spline")

        ################################################# Bezier #################################################
        self.frame_bezier = Frame(self.cb, borderwidth=1, relief="raised", bg="gray")
        self.frame_bezier.place(x=0, y=0, width=300, height=300)

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
        Label(self.frame_bezier, bg="gray", text="Z1:").place(x=198, y=50)
        self.cbZ1 = Entry(self.frame_bezier, width=5)
        self.cbZ1.place(x=220, y=50)
        #ponto 2
        Label(self.frame_bezier, bg="gray", text="X2:").place(x=2, y=80)
        self.cbX2 = Entry(self.frame_bezier, width=5)
        self.cbX2.place(x=30, y=80)
        Label(self.frame_bezier, bg="gray", text="Y2:").place(x=100, y=80)
        self.cbY2 = Entry(self.frame_bezier, width=5)
        self.cbY2.place(x=125, y=80)
        Label(self.frame_bezier, bg="gray", text="Z2:").place(x=198, y=80)
        self.cbZ2 = Entry(self.frame_bezier, width=5)
        self.cbZ2.place(x=220, y=80)
        #ponto 3
        Label(self.frame_bezier, bg="gray", text="X3:").place(x=2, y=110)
        self.cbX3 = Entry(self.frame_bezier, width=5)
        self.cbX3.place(x=30, y=110)
        Label(self.frame_bezier, bg="gray", text="Y3:").place(x=100, y=110)
        self.cbY3 = Entry(self.frame_bezier, width=5)
        self.cbY3.place(x=125, y=110)
        Label(self.frame_bezier, bg="gray", text="Z3:").place(x=198, y=110)
        self.cbZ3 = Entry(self.frame_bezier, width=5)
        self.cbZ3.place(x=220, y=110)
        #ponto 4
        self.empty_frame = Frame(self.frame_bezier, bg="gray", width=300, height=30) #Frame vazio que sera levantado após a primeira inserção de pontos
        self.empty_frame.place(x=0, y=140)
        #frame inicial para 4 pontos de entrada
        self.p4_frame = Frame(self.frame_bezier, bg="gray", width=300, height=30)
        self.p4_frame.place(x=0, y=140)
        Label(self.p4_frame, bg="gray", text="X4:").place(x=2, y=0)
        self.cbX4 = Entry(self.p4_frame, width=5)
        self.cbX4.place(x=30, y=0)
        Label(self.p4_frame, bg="gray", text="Y4:").place(x=100, y=0)
        self.cbY4 = Entry(self.p4_frame, width=5)
        self.cbY4.place(x=125, y=0)
        Label(self.p4_frame, bg="gray", text="Z4:").place(x=198, y=0)
        self.cbZ4 = Entry(self.p4_frame, width=5)
        self.cbZ4.place(x=220, y=0)
        
        Button(self.frame_bezier, text="ADICIONAR", command=lambda:self.add_pontos_curvB()).place(x=0, y=185)
        Button(self.frame_bezier, text="CONCLUIR", command=lambda:self.criar_curva("B")).place(x=100, y=185)

        self.msg_label4 = Label(self.frame_bezier, text="", bg="gray")
        self.msg_label4.place(x=10, y=215)

        ################################################# Spline #################################################
        self.frame_spline = Frame(self.cs, borderwidth=1, relief="raised", bg="gray")
        self.frame_spline.place(x=0, y=0, width=300, height=300)

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
        Label(self.frame_spline, bg="gray", text="Z1:").place(x=198, y=50)
        self.csZ1 = Entry(self.frame_spline, width=5)
        self.csZ1.place(x=220, y=50)
        #ponto 2
        self.empty_frameCS = Frame(self.frame_spline, bg="gray", width=300, height=90) #Frame vazio que sera levantado após a primeira inserção de pontos
        self.empty_frameCS.place(x=0, y=80)
        self.p_frame = Frame(self.frame_spline, bg="gray", width=300, height=90)
        self.p_frame.place(x=0, y=80)
        #frame inicial para 4 pontos de entrada        
        Label(self.p_frame, bg="gray", text="X2:").place(x=2, y=0)
        self.csX2 = Entry(self.p_frame, width=5)
        self.csX2.place(x=30, y=0)
        Label(self.p_frame, bg="gray", text="Y2:").place(x=100, y=0)
        self.csY2 = Entry(self.p_frame, width=5)
        self.csY2.place(x=125, y=0)
        Label(self.p_frame, bg="gray", text="Z2:").place(x=198, y=0)
        self.csZ2 = Entry(self.p_frame, width=5)
        self.csZ2.place(x=220, y=0)
        #ponto 3
        Label(self.p_frame, bg="gray", text="X3:").place(x=2, y=30)
        self.csX3 = Entry(self.p_frame, width=5)
        self.csX3.place(x=30, y=30)
        Label(self.p_frame, bg="gray", text="Y3:").place(x=100, y=30)
        self.csY3 = Entry(self.p_frame, width=5)
        self.csY3.place(x=125, y=30)
        Label(self.p_frame, bg="gray", text="Z3:").place(x=198, y=30)
        self.csZ3 = Entry(self.p_frame, width=5)
        self.csZ3.place(x=220, y=30)
        #ponto 4
        Label(self.p_frame, bg="gray", text="X4:").place(x=2, y=60)
        self.csX4 = Entry(self.p_frame, width=5)
        self.csX4.place(x=30, y=60)
        Label(self.p_frame, bg="gray", text="Y4:").place(x=100, y=60)
        self.csY4 = Entry(self.p_frame, width=5)
        self.csY4.place(x=125, y=60)
        Label(self.p_frame, bg="gray", text="Z4:").place(x=198, y=60)
        self.csZ4 = Entry(self.p_frame, width=5)
        self.csZ4.place(x=220, y=60)

        
        Button(self.frame_spline, text="ADICIONAR", command=lambda:self.add_pontos_curvS()).place(x=0, y=185)
        Button(self.frame_spline, text="CONCLUIR", command=lambda:self.criar_curva("S")).place(x=100, y=185)

        self.msg_label5 = Label(self.frame_spline, text="", bg="gray")
        self.msg_label5.place(x=10, y=215)

        ################################################# ARAME ###################################################
        self.arame_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=300, height=300)
        self.arame_frame.place(x=100, y=0)

        Label(self.arame_frame, bg="gray", text="Nome :").place(x=2, y=5)
        self.nome_obj6 = Entry(self.arame_frame, width=12)
        self.nome_obj6.place(x=50, y=5)
        
        self.scroll_frameE = Frame(self.arame_frame, bg="black")
        self.scroll_frameE.place(x=100, y=35, height=230)
        self.scrollbarE = Scrollbar(self.scroll_frameE, orient=VERTICAL)

        self.scroll_frameD = Frame(self.arame_frame, bg="black")
        self.scroll_frameD.place(x=280, y=35, height=230)
        self.scrollbarD = Scrollbar(self.scroll_frameD, orient=VERTICAL)

        self.obj_copy = Listbox(self.arame_frame, bg="gray40", yscrollcommand=self.scrollbarE.set) 
        self.scrollbarE.config(command=self.obj_copy.yview)
        self.scrollbarE.pack(side=RIGHT, fill=Y)
        self.obj_copy.place(x=10, y=35, width=90 , height=230)

        self.arame_list = Listbox(self.arame_frame, bg="gray40", yscrollcommand=self.scrollbarD.set) 
        self.scrollbarD.config(command=self.arame_list.yview)
        self.scrollbarD.pack(side=RIGHT, fill=Y)
        self.arame_list.place(x=190, y=35, width=90 , height=230)
        
        self.copy_listbox(self.w.object_list, self.obj_copy)

        Button(self.arame_frame, text="->", width=2, command=lambda:self.add_from_to(self.obj_copy, self.arame_list)).place(x=125,y=80)
        Button(self.arame_frame, text="<-", width=2, command=lambda:self.add_from_to(self.arame_list, self.obj_copy)).place(x=125,y=120)
        Button(self.arame_frame, text="Ok", width=2, command=lambda:self.criar_arame()).place(x=125,y=160)

        self.msg_label6 = Label(self.arame_frame, text="", bg="gray")
        self.msg_label6.place(x=10, y=270)

        ######################################################### Superficie #############################################################
        self.cont = 16
        
        self.superf_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=300, height=300)
        self.superf_frame.place(x=100, y=0) 
        Label(self.superf_frame, bg="gray", text="Nome :").place(x=5, y=5)
        self.nome_superf = Entry(self.superf_frame, width=12)
        self.nome_superf.place(x=52, y=5)
        Label(self.superf_frame, bg="gray", text="X :").place(x=5, y=50)
        self.supX = Entry(self.superf_frame, width=5)
        self.supX.place(x=25, y=50)
        Label(self.superf_frame, bg="gray", text="Y :").place(x=100, y=50)
        self.supY = Entry(self.superf_frame, width=5)
        self.supY.place(x=120, y=50)
        Label(self.superf_frame, bg="gray", text="Z :").place(x=195, y=50)
        self.supZ = Entry(self.superf_frame, width=5)
        self.supZ.place(x=215, y=50)
        Button(self.superf_frame, text="ADICIONAR", command=lambda:self.add_ponto_superf()).place(x=50, y=100)
        self.msgInf_label = Label(self.superf_frame, textvariable=self.w.sup_msg, bg="gray", foreground="black")
        self.msgInf_label.place(x=10, y=150)
        self.msgErr_label = Label(self.superf_frame, text="", bg="gray")
        self.msgErr_label.place(x=10, y=200)


        ######################################################## INICIAL ###################################################################
        self.pop_padrao = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=300, height=300)
        self.pop_padrao.place(x=100, y=0) 
        Label(self.pop_padrao, text="Selecione objeto que \n quer desenhar!", bg="gray").place(x=50, y=120)


    def add_ponto_superf(self):
        try:
            nome = self.nome_superf.get()
            if not (nome in self.w.obj_dict.keys()):
                x = float(self.supX.get())            #cuida que x e y nao recebeu entrada de string
                y = float(self.supY.get())
                z = float(self.supZ.get())
                self.w.pontos_sup.append((x,y,z))
                
                self.cont = 16-len(self.w.pontos_sup)
                self.w.sup_msg.set(f"Adicione mais {self.cont} pontos")
                #self.msgInf_label.config(text=mensagem, foreground="black")
                self.msgErr_label.config(text="")
                if self.cont == 0:
                    self.criar_superficie()
            else:
                self.w.sup_msg.set("Ponto não adicionado")
                self.msgErr_label.config(text="Nome já existente!", foreground="red")
        except:
            self.msgErr_label.config(text="Apenas números!", foreground="red")
    
    def criar_superficie(self):
        nome = self.nome_superf.get()
        self.w.object_list.insert(END, nome)
        pontos = self.w.pontos_sup[:]                 #copia a lista
        self.w.obj_dict[nome] = Superficie(nome, pontos) 
        self.w.pontos_sup = []
        self.w.obj_dict[nome].moverXY(self.w.mathomo, True)
        mat = self.w.gerarDescricaoSCN()              #gerar descricao de SCN
        self.w.obj_dict[nome].normalize(mat)          #normaliza objeto criado
        var = self.w.clip_selection.get()
        self.w.obj_dict[nome].superf_clipping(var)
        self.w.sup_msg.set("Superficie criado!")
        self.w.redesenhar()


    def add_from_to(self, origem, destino):
        if len(origem.curselection()) == 1:
            chave = origem.get(origem.curselection())
            index = origem.get(0, "end").index(chave)
            origem.delete(index)
            destino.insert(END, chave)

    def copy_listbox(self, origem, destino):
        for i in origem.get(0, END):
            destino.insert(END, i)

    def criar_arame(self):
        #try:
        nome = self.nome_obj6.get()
        if not (nome in self.w.obj_dict.keys()):
            self.w.object_list.insert(END, nome)
            obj_list = []
            for obj in self.arame_list.get(0, END):
                if self.w.obj_dict[obj].tipo == 1 or self.w.obj_dict[obj].tipo == 2 or self.w.obj_dict[obj].tipo == 5: #se ponto ou linha ou curva
                    obj_list.append(self.w.obj_dict[obj])
                elif self.w.obj_dict[obj].tipo == 3: # se eh poligono
                    for i in range(len(self.w.obj_dict[obj].coordenadas)): #adicionamos todas as linhas do polígono e as tratamos individualmente (melhor calculo do centro)
                        obj_list.append(Line(f"{self.w.obj_dict[obj].nome}_{i}",[self.w.obj_dict[obj].coordenadas[i-1], self.w.obj_dict[obj].coordenadas[i]]))
                elif self.w.obj_dict[obj].tipo == 6: # se eh outro arame
                    for i in self.w.obj_dict[obj].obj_list:
                        obj_list.append(i)
                index = self.w.object_list.get(0, "end").index(obj)
                self.w.object_list.delete(index)
                del self.w.obj_dict[obj]            #del self.w.obj_dict[self.w.object_list.get(index)] 
            
            self.w.obj_dict[nome] = Arame(nome, obj_list) 
            self.w.obj_dict[nome].moverXY(self.w.mathomo, True) #Necessário para o caso do polígono, onde as novas Line's sendo criadas precisam ter coordNorm para sua normalização
            mat = self.w.gerarDescricaoSCN()             #gera descricao de SCN
            self.w.obj_dict[nome].normalize(mat)         #normaliza objeto criado
            tipo = self.w.clip_selection.get()
            self.w.obj_dict[nome].arame_clipping(tipo)
            self.w.redesenhar()
        
            self.arame_list.delete(0, END)  #apaga os objetos que agora fazem parte de um arame
        else:
            self.msg_label6.config(text="Nome já existente!", foreground="red")
        #except:
        #    self.msg_label6.config(text="Ocorreu um erro... Desculpe", foreground="red")


    def criar_ponto(self):
        try:
            nome = self.nome_point.get()
            if not (nome in self.w.obj_dict.keys()):         #verifica se nao tem o objeto com mesmo nome 
                x = float(self.px.get())            #cuida que x e y nao recebeu entrada de string
                y = float(self.py.get())
                z = float(self.pz.get())
                self.w.object_list.insert(END, nome)         #insere o nome do objeto na listbox
                self.w.obj_dict[nome] = Point(nome, [(x,y,z)]) #adiciona o ponto no dicionario de objetos, chave = nome
                self.w.obj_dict[nome].moverXY(self.w.mathomo, True) #projecao 
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
                z1 = float(self.lz1.get())
                
                x2 = float(self.lx2.get())
                y2 = float(self.ly2.get())
                z2 = float(self.lz2.get())
                self.w.object_list.insert(END, nome)                  #insere o nome do objeto na listbox
                self.w.obj_dict[nome] = Line(nome, [(x1,y1,z1),(x2,y2,z2)]) #adiciona a linha no dicionario de objetos, chave = nome
                self.w.obj_dict[nome].moverXY(self.w.mathomo, True) #projecao 
                mat = self.w.gerarDescricaoSCN()  
                self.w.obj_dict[nome].normalize(mat)
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
            z = float(self.polz.get())
            self.w.pontos_pol.append((x,y,z))
            self.msg_label3.config(text="Ponto adicionado!", foreground="SpringGreen2")
        except:
            self.msg_label3.config(text="Apenas números!", foreground="red")

    #quando usuario concluir adicao de pontos, vai criar poligono
    def criar_poligono(self):
        nome = self.nome_poly.get()
        if not (nome in self.w.obj_dict.keys()):          #verifica se nao tem o objeto com mesmo nome
            self.w.object_list.insert(END, nome)
            pontos = self.w.pontos_pol[:]                 #copia a lista
            self.w.obj_dict[nome] = Polygon(nome, pontos)
            self.w.pontos_pol = []
            self.w.obj_dict[nome].moverXY(self.w.mathomo, True)
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
            pontos = self.w.pontos_curvaB[:]
            self.w.pontos_curvaB = []
        else:
            nome = self.nome_obj5.get() #Spline
            pontos = self.w.pontos_curvaS[:]
            self.w.pontos_curvaS = []
        
        if not (nome in self.w.obj_dict.keys()):          #verifica se nao tem o objeto com mesmo nome
            self.w.object_list.insert(END, nome)                
            #self.w.obj_dict[nome].moverXY(self.w.mathomo, True)   talvez um control V aqui do nada, não fazemos ideia do porque dessa linha...
            mat = self.w.gerarDescricaoSCN()              #gerar descricao de SCN
            self.w.obj_dict[nome] = Curve(nome, pontos, mat, tipo)    #curva já tem seus pontos normalizados na criação
            #self.obj_dict[nome].normalize(mat)          #normaliza objeto criado
            var = self.w.clip_selection.get()
            self.w.obj_dict[nome].curv_clipping(var)
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
            z1 = float(self.cbZ1.get())
            x2 = float(self.cbX2.get()) #cuida que x e y nao recebeu entrada de string
            y2 = float(self.cbY2.get())
            z2 = float(self.cbZ2.get())
            x3 = float(self.cbX3.get()) #cuida que x e y nao recebeu entrada de string
            y3 = float(self.cbY3.get())
            z3 = float(self.cbZ3.get())
            if not self.w.pontos_curvaB:
                x4 = float(self.cbX4.get()) #cuida que x e y nao recebeu entrada de string
                y4 = float(self.cbY4.get())
                z4 = float(self.cbZ4.get())
                adicionar = True
            self.w.pontos_curvaB.append((x1,y1,z1))
            self.w.pontos_curvaB.append((x2,y2,z2))
            self.w.pontos_curvaB.append((x3,y3,z3))
            if adicionar:
                self.w.pontos_curvaB.append((x4,y4,z4))

            self.w.levantar_frame(self.empty_frame, zerar=False)
            self.msg_label4.config(text="Ponto adicionado!", foreground="SpringGreen2")
        except:
            self.msg_label4.config(text="Apenas números!", foreground="red")

    def add_pontos_curvS(self):
        try:
            adicionar = False
            x1 = float(self.csX1.get()) #cuida que x e y nao recebeu entrada de string
            y1 = float(self.csY1.get())
            z1 = float(self.csZ1.get())
            if not self.w.pontos_curvaS:
                x2 = float(self.csX2.get()) 
                y2 = float(self.csY2.get())
                z2 = float(self.csZ2.get())
                x3 = float(self.csX3.get()) 
                y3 = float(self.csY3.get())
                z3 = float(self.csZ3.get())
                x4 = float(self.csX4.get()) #cuida que x e y nao recebeu entrada de string
                y4 = float(self.csY4.get())
                z4 = float(self.csZ4.get())
                adicionar = True
            self.w.pontos_curvaS.append((x1,y1,z1))
            if adicionar:
                self.w.pontos_curvaS.append((x2,y2,z2))
                self.w.pontos_curvaS.append((x3,y3,z3))
                self.w.pontos_curvaS.append((x4,y4,z4))

            self.w.levantar_frame(self.empty_frameCS, zerar=False)
            self.msg_label5.config(text="Ponto adicionado!", foreground="SpringGreen2")
        except:
            self.msg_label5.config(text="Apenas números!", foreground="red")

        
'''
import tkinter as tk

root = tk.Tk()

# criar uma variável StringVar e atribuir ela como valor para a opção textvariable do Label
var_text = tk.StringVar(value="Olá, mundo!")
label = tk.Label(root, textvariable=var_text)
label.pack()

# função para atualizar o valor da variável StringVar
def atualizar_texto():
    var_text.set("Novo texto!")

# botão para chamar a função que atualiza o texto
botao = tk.Button(root, text="Atualizar texto", command=atualizar_texto)
botao.pack()

root.mainloop()
'''
