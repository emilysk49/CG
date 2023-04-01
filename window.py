from tkinter import *
from tkinter import ttk
from point import Point
from line import Line
from polygon import Polygon
from win import Win
import numpy as np
import string
from PIL import Image, ImageTk


class Window():
    def __init__(self):
        self.main_window = Tk()
        self.main_window.geometry("930x700+450+200")
        self.main_window.title("Computer Graphic")
        self.main_window["bg"]= "gray"

        #relief opcoes: solid, flat, raised, sunken
        #Frame das opcoes escontradas na esquerda da tela
        self.dFile_frame = Frame(self.main_window, borderwidth=1, relief="raised", bg="gray")
        self.dFile_frame.place(x=10, y=10, width=200, height=670)

        #canvas referente a viewport
        self.canvas = Canvas(self.main_window, width=570, height=570, bg="floral white")
        self.canvas.place(x=230, y=10)
        
        #valores iniciais/escala da window, indo de x=-11 até 11, idem ao y


        self.windowObj = Win("Window")

        #self.xwMin = -11
        #self.xwMax = 11
        #self.ywMin = -11
        #self.ywMax = 11

        #tamanho da tela do viewport (canvas)
        self.xvMin = 0
        self.xvMax = 570
        self.yvMin = 0
        self.yvMax = 570

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
        self.obj_dict = {}
        self.scrollbar.config(command=self.object_list.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.object_list.place(x=10, y=20, width=155 , height=125)

        #botao para apagar objeto existente
        self.apagarB = Button(self.dFile_frame, text="Delete", command=lambda:self.apagar_objeto())
        self.apagarB.place(x=70, y=155, width=60)
        #botao para adicionar objeto novo -> abre um popup
        self.objectB = Button(self.dFile_frame, text="Add", command=lambda:self.criar_objeto())
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

        #self.direita = PhotoImage(file="image/direita.gif")
        #self.esquerda = PhotoImage(file="image/esquerda.gif")
        self.esquerda = ImageTk.PhotoImage(Image.open("image/esquerda.png").resize((30,30), Image.ANTIALIAS))
        self.direita = ImageTk.PhotoImage(Image.open("image/direita.png").resize((30,30), Image.ANTIALIAS))

        Button(self.tool_frame, image=self.direita, command=lambda:self.rotacionarWin(-15)).place(x=85, y=160)
        Button(self.tool_frame, image=self.esquerda, command=lambda:self.rotacionarWin(15)).place(x=45, y=160)

        self.eixoX = Line("x", [(-100,0), (100,0)])
        self.eixoY = Line("y", [(0,-100), (0, 100)])

        #Como a window é iniciada no meio não precisamos normalizar nem nada, escolhemos os valores já normalizados padroes dos limites do viewport
        self.canvas.create_line(self.xvp(-1), self.yvp(0), self.xvp(1), self.yvp(0), fill="black", width=3)
        self.canvas.create_line(self.xvp(0), self.yvp(-1), self.xvp(0), self.yvp(1), fill="black", width=3)


        #Button(self.tool_frame, image=self.direita).place(x=20, y=140)

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

        #duas linhas eixo x e y para criar plano cartesiano
        #self.canvas.create_line(self.xvp(0), self.yvMax, self.xvp(0), self.yvMin, fill="gray", width=2, arrow=BOTH)
        #self.canvas.create_line(self.xvMin, self.yvp(0), self.xvMax, self.yvp(0), fill="gray", width=2, arrow=BOTH)
        #posicoes 10 em x e y e -10 para referencia

        #self.canvas.create_text(self.xvp(10),self.yvp(1), text="10", fill="black")
        #self.canvas.create_text(self.xvp(1),self.yvp(10), text="10", fill="black")
        #self.canvas.create_text(self.xvp(-1),self.yvp(-10), text="-10", fill="black")
        #self.canvas.create_text(self.xvp(-10),self.yvp(-1), text="-10", fill="black")

    #transformada de viewport x
    def xvp(self, xw):
        #return ( ((xw-self.xwMin)/(self.xwMax - self.xwMin))*(self.xvMax-self.xvMin) )
        return ( (xw-(-1))/(1-(-1))*(self.xvMax-self.xvMin)  )
        

    #transformada de viewport y
    def yvp(self, yw):
        #return ( (1-((yw-self.ywMin)/(self.ywMax-self.ywMin)))*(self.yvMax-self.yvMin) )
        return ( (1-((yw-(-1))/(1-(-1))))*(self.yvMax-self.yvMin) )
    
    #para esquerda <- diminui os x's
    def left(self):
        #self.xwMin -= 1 
        #self.xwMax -= 1
        mat = [[1,0,0],[0,1,0],[-1,0,1]]
        self.windowObj.moverXY(mat)
        self.normalizar()
        #chamar uma func normalizar que vai chamar o gerarDescricaoSCN para cada objeto
        self.redesenhar()

    #para direita -> aumenta os x's
    def right(self):
        #self.xwMax += 1
        #self.xwMin += 1
        mat = [[1,0,0],[0,1,0],[1,0,1]]
        self.windowObj.moverXY(mat)
        self.normalizar()
        self.redesenhar()

    #para cima ↑ aumenta os y's
    def up(self):
        #self.ywMax += 1
        #self.ywMin += 1
        mat = [[1,0,0],[0,1,0],[0,1,1]]
        self.windowObj.moverXY(mat)
        self.normalizar()
        self.redesenhar()

    #para baixo ↓ diminui os y's
    def down(self):
        #self.ywMax -= 1
        #self.ywMin -= 1
        mat = [[1,0,0],[0,1,0],[0,-1,1]]
        self.windowObj.moverXY(mat)
        self.normalizar()
        self.redesenhar()

    #zoomin -> aproxima os pontos da window
    def zoomIn(self):
        #Verificacao para nao inverter a tela com muito zoomIn (rever para possiveis diferentes niveis de zoom)
        mat = [[0.9, 0, 0],[0, 0.9, 0],[0, 0, 1]]
        self.windowObj.moverXY(mat)
        self.normalizar()
        self.redesenhar()
    
    #zoomout -> afasta os pontos da window
    def zoomOut(self):
        mat = [[1.1, 0, 0],[0, 1.1, 0],[0, 0, 1]]
        self.windowObj.moverXY(mat)
        self.normalizar()
        self.redesenhar()



    def redesenhar(self):
        self.canvas.delete("all") #primeiro apaga tudo

        #vai verificar se tem objeto para redesenhar
        for obj in self.obj_dict.values():

            tup = obj.coordNorm
            
            if obj.tipo == 1: #se ponto
                self.canvas.create_oval(self.xvp(tup[0][0])-3, self.yvp(tup[0][1])-3, self.xvp(tup[0][0])+3, self.yvp(tup[0][1])+3, fill=obj.cor)

            elif obj.tipo == 2: #se linha
                self.canvas.create_line(self.xvp(tup[0][0]), self.yvp(tup[0][1]), self.xvp(tup[1][0]), self.yvp(tup[1][1]), fill=obj.cor, width=3)

            elif obj.tipo == 3: #se poligono
                for i in range (len(tup)):
                    self.canvas.create_line(self.xvp(tup[i][0]), self.yvp(tup[i][1]), self.xvp(tup[i-1][0]), self.yvp(tup[i-1][1]), fill=obj.cor, width=3)
                
        #duas linhas eixo x e y para criar plano cartesiano
        #self.canvas.create_line(self.xvp(0), self.yvMax, self.xvp(0), self.yvMin, fill="gray", width=2, arrow=BOTH)
        #self.canvas.create_line(self.xvMin, self.yvp(0), self.xvMax, self.yvp(0), fill="gray", width=2, arrow=BOTH)
        self.canvas.create_line(self.xvp(self.eixoX.coordNorm[0][0]), self.yvp(self.eixoX.coordNorm[0][1]), self.xvp(self.eixoX.coordNorm[1][0]), self.yvp(self.eixoX.coordNorm[1][1]), fill="black", width=3)
        self.canvas.create_line(self.xvp(self.eixoY.coordNorm[0][0]), self.yvp(self.eixoY.coordNorm[0][1]), self.xvp(self.eixoY.coordNorm[1][0]), self.yvp(self.eixoY.coordNorm[1][1]), fill="black", width=3)
        #posicoes 10 em x e y e -10 para referencia
        '''
        self.canvas.create_text(self.xvp(10),self.yvp(1), text="10")
        self.canvas.create_text(self.xvp(1),self.yvp(10), text="10")
        self.canvas.create_text(self.xvp(-1),self.yvp(-10), text="-10")
        self.canvas.create_text(self.xvp(-10),self.yvp(-1), text="-10")
        '''
        
    def criar_ponto(self):
        try:
            nome = self.nome_obj.get()
            if not (nome in self.obj_dict.keys()): #verifica se nao tem o objeto com mesmo nome 
                x = float(self.entrada_x.get()) #cuida que x e y nao recebeu entrada de string
                y = float(self.entrada_y.get())
                self.object_list.insert(END, nome) #insere o nome do objeto na listbox
                self.obj_dict[nome] = Point(nome, [(x,y)]) #adiciona o ponto no dicionario de objetos, chave = nome
                mat = self.gerarDescricaoSCN()
                self.obj_dict[nome].normalize(mat)
                self.redesenhar()
                self.msg_label.config(text="Ponto adicionado!", foreground="SpringGreen2")
            else:
                self.msg_label.config(text="Nome já existente!", foreground="red")
        except:
            self.msg_label.config(text="Apenas números!", foreground="red")

    def criar_linha(self):
        try:
            nome = self.nome_obj2.get()
            if not (nome in self.obj_dict.keys()): #verifica se nao tem o objeto com mesmo nome
                x1 = float(self.entrada_x1.get()) #cuida se x e y nao recebeu entrada de string
                y1 = float(self.entrada_y1.get())

                x2 = float(self.entrada_x2.get())
                y2 = float(self.entrada_y2.get())

                self.object_list.insert(END, nome) #insere o nome do objeto na listbox
                self.obj_dict[nome] = Line(nome, [(x1,y1),(x2,y2)]) #adiciona a linha no dicionario de objetos, chave = nome
                mat = self.gerarDescricaoSCN()
                self.obj_dict[nome].normalize(mat)
                self.redesenhar()
                self.msg_label2.config(text="Linha adicionada!", foreground="SpringGreen2")
            else:
                self.msg_label2.config(text="Nome já existente!", foreground="red")
        except:
            self.msg_label2.config(text="Apenas números!", foreground="red")

    #enquanto usuario nao concluir, vai adicionado pontos para criacao de poligono
    def add_ponto_pol(self):
        try:
            x = float(self.entrada_x3.get()) #cuida que x e y nao recebeu entrada de string
            y = float(self.entrada_y3.get())
            self.pontos_pol.append((x,y))
            self.msg_label3.config(text="Ponto adicionado!", foreground="SpringGreen2")
        except:
            self.msg_label3.config(text="Apenas números!", foreground="red")

    #quando usuario concluir adicao de pontos, vai criar poligono
    def criar_poligono(self):
        nome = self.nome_obj3.get()
        if not (nome in self.obj_dict.keys()): #verifica se nao tem o objeto com mesmo nome
            self.object_list.insert(END, nome)
            pontos = self.pontos_pol[:] #copia a lista
            self.obj_dict[nome] = Polygon(nome, pontos)
            self.pontos_pol = []
            mat = self.gerarDescricaoSCN()
            self.obj_dict[nome].normalize(mat)
            self.redesenhar()
            self.msg_label3.config(text="Polígono criado!", foreground="SpringGreen2")
        else:
            self.msg_label3.config(text="Nome já existente!", foreground="red")


    def apagar_objeto(self):
        #verifica linha onde cursor selecionou
        for linha in self.object_list.curselection():  
            #apaga do dicionario e do list box esse objeto selecionado
            del self.obj_dict[self.object_list.get(linha)] 
            self.object_list.delete(linha)
        self.redesenhar()

    #utilizado para criacao de objetos podendo seleciona varias frames para preencher
    def levantar_frame(self, frame:Frame):
        self.pontos_pol = [] #Ao trocar para outra entrada perde-se o progresso
        frame.tkraise()

    def criar_objeto(self):
        self.pop = Toplevel(self.main_window)
        self.pop.geometry("300x300+450+200")
        self.pop.title("Create New Object")
        self.pop.config(bg="gray")

        #Botoes para selecionar qual objeto adicionar
        Button(self.pop, text="Point", width=5, command=lambda:self.levantar_frame(self.point_frame)).place(x=10, y=10)
        Button(self.pop, text="Line", width=5, command=lambda:self.levantar_frame(self.line_frame)).place(x=10, y=40)
        Button(self.pop, text="Polygon", width=5, command=lambda:self.levantar_frame(self.polygon_frame)).place(x=10, y=70)

        #frame ponto pop up
        self.point_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.point_frame.place(x=100, y=0) 
        Label(self.point_frame, bg="gray", text="Nome :").place(x=5, y=5)
        self.nome_obj = Entry(self.point_frame, width=12)
        self.nome_obj.place(x=52, y=5)
        Label(self.point_frame, bg="gray", text="X :").place(x=5, y=50)
        self.entrada_x = Entry(self.point_frame, width=5)
        self.entrada_x.place(x=25, y=50)
        Label(self.point_frame, bg="gray", text="Y :").place(x=100, y=50)
        self.entrada_y = Entry(self.point_frame, width=5)
        self.entrada_y.place(x=120, y=50)
        Button(self.point_frame, text="CONCLUIR", command=lambda:self.criar_ponto()).place(x=50, y=100)
        self.msg_label = Label(self.point_frame, text="", bg="gray")
        self.msg_label.place(x=10, y=150)

        #frame linha pop up
        self.line_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.line_frame.place(x=100, y=0) 
        Label(self.line_frame, bg="gray", text="Nome :").place(x=5, y=5)
        self.nome_obj2 = Entry(self.line_frame, width=12)
        self.nome_obj2.place(x=52, y=5)
        Label(self.line_frame, bg="gray", text="X1 :").place(x=5, y=50)
        self.entrada_x1 = Entry(self.line_frame, width=5)
        self.entrada_x1.place(x=32, y=50)
        Label(self.line_frame, bg="gray", text="Y1 :").place(x=100, y=50)
        self.entrada_y1 = Entry(self.line_frame, width=5)
        self.entrada_y1.place(x=127, y=50)
        Label(self.line_frame, bg="gray", text="X2 :").place(x=5, y=80)
        self.entrada_x2 = Entry(self.line_frame, width=5)
        self.entrada_x2.place(x=32, y=80)
        Label(self.line_frame, bg="gray", text="Y2 :").place(x=100, y=80)
        self.entrada_y2 = Entry(self.line_frame, width=5)
        self.entrada_y2.place(x=127, y=80)
        Button(self.line_frame, text="CONCLUIR", command=lambda:self.criar_linha()).place(x=50, y=150)
        self.msg_label2 = Label(self.line_frame, text="", bg="gray")
        self.msg_label2.place(x=10, y=180)

        #frame poligono pop up
        self.polygon_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.polygon_frame.place(x=100, y=0) 
        Label(self.polygon_frame, bg="gray", text="Nome :").place(x=5, y=5)
        self.nome_obj3 = Entry(self.polygon_frame, width=12)
        self.nome_obj3.place(x=52, y=5)
        Label(self.polygon_frame, bg="gray", text="X :").place(x=5, y=50)
        self.entrada_x3 = Entry(self.polygon_frame, width=5)
        self.entrada_x3.place(x=25, y=50)
        Label(self.polygon_frame, bg="gray", text="Y :").place(x=100, y=50)
        self.entrada_y3 = Entry(self.polygon_frame, width=5)
        self.entrada_y3.place(x=120, y=50)
        Button(self.polygon_frame, text="ADICIONAR", command=lambda:self.add_ponto_pol()).place(x=0, y=100)
        Button(self.polygon_frame, text="CONCLUIR", command=lambda:self.criar_poligono()).place(x=100, y=100)
        self.msg_label3 = Label(self.polygon_frame, text="", bg="gray")
        self.msg_label3.place(x=10, y=150)

        #Janela pop-up inicial
        self.pop_padrao = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.pop_padrao.place(x=100, y=0) 
        Label(self.pop_padrao, text="Selecione objeto que \n quer desenhar!", bg="gray").place(x=30, y=120)


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
            
            Label(self.ftb1, bg="gray", text="DY:").place(x=150, y=50)
            self.entrada_dy = Entry(self.ftb1, width=5)
            self.entrada_dy.place(x=175, y=50)

            self.trans_msg = Label(self.ftb1, text="", bg="gray")
            self.trans_msg.place(x=10, y=100)


            ################### Tab2 (Escalonamento) ###################
            self.ftb2 = Frame(self.tb2, borderwidth=1, relief="raised", bg="gray")
            self.ftb2.place(x=7, y=5, width=330, height=300)

            Label(self.ftb2, bg="gray", text="Escalonar por:").place(x=5, y=5)

            Label(self.tb2, bg="gray", text="SX:").place(x=10, y=50)
            self.entrada_sx = Entry(self.tb2, width=5)
            self.entrada_sx.place(x=35, y=50)
            
            Label(self.tb2, bg="gray", text="SY:").place(x=150, y=50)
            self.entrada_sy = Entry(self.tb2, width=5)
            self.entrada_sy.place(x=175, y=50)

            self.scale_msg = Label(self.ftb2, text="", bg="gray")
            self.scale_msg.place(x=10, y=100)


            ################### Tab3 (Rotação) ###################
            self.ftb3 = Frame(self.tb3, borderwidth=1, relief="raised", bg="gray")
            self.ftb3.place(x=7, y=5, width=330, height=300)

            self.select = Frame(self.ftb3, borderwidth=1, relief="raised", bg="gray")
            self.select.place(x=10, y=5, width=310, height=130)

            Label(self.select, bg="gray", text="Opções:").place(x=5, y=5)

            self.option = StringVar()   #Tipo necessário para auxiliar a retirada da opção do Radiobutton

            
            Label(self.ftb3, bg="gray", text="Ângulo:").place(x=20, y=150)
            self.entrada_grau = Entry(self.ftb3, width=5)
            self.entrada_grau.place(x=72, y=150)
            Label(self.ftb3, bg="gray", text="°").place(x=130, y=150)


            self.fr_point = Frame(self.ftb3, borderwidth=1, relief="raised", bg="gray")
            self.fr_point.place(x=10, y=180, width=310, height=100)

            self.fr_general = Frame(self.ftb3, bg="gray")
            self.fr_general.place(x=10, y=180, width=310 , height=100)

            self.general_msg = Label(self.fr_general, text="", bg="gray")
            self.general_msg.place(x=10, y=10)
            
            Label(self.fr_point, bg="gray", text="X:").place(x=10, y=10)
            self.entrada_xp = Entry(self.fr_point, width=5)
            self.entrada_xp.place(x=35, y=10)

            self.point_msg = Label(self.fr_point, text="", bg="gray")
            self.point_msg.place(x=10, y=50)
            
            Label(self.fr_point, bg="gray", text="Y:").place(x=150, y=10)
            self.entrada_yp = Entry(self.fr_point, width=5)
            self.entrada_yp.place(x=175, y=10)

            #Radiobutton são as partes de click para selecionar opção
            rb = Radiobutton(self.select, text="Rotacionar sobre origem", value="o", variable=self.option, bg="gray", command=lambda:self.levantar_frame(self.fr_general))
            rb.place(x=5,y=35)
            rb2 = Radiobutton(self.select, text="Rotacionar sobre ponto", value="p", variable=self.option, bg="gray",  command=lambda:self.levantar_frame(self.fr_point))
            rb2.place(x=5,y=65)
            rb3 = Radiobutton(self.select, text="Rotacionar sobre centro do objeto", value="s", variable=self.option, bg="gray",  command=lambda:self.levantar_frame(self.fr_general))
            rb3.place(x=5,y=95)
         

    def transformar(self, tab):
        if tab == "Translação":
            try:
                dx = float(self.entrada_dx.get())   #translação em relação ao eixo X
                dy = float(self.entrada_dy.get())   #translação em relação ao eixo Y
                self.historico.insert(END, f"t {dx} {dy}")  #insersão na listbox de transformações
                self.trans_msg.config(text="Translação adicionada ao histórico", foreground="SpringGreen2")
            except:
                self.trans_msg.config(text="Números Inválidos", foreground="Red")
                
        elif tab == "Escalonamento":
            try:
                sx = float(self.entrada_sx.get())   #Escalonamento para o ponto no eixo X
                sy = float(self.entrada_sy.get())   #Escalonamento para o ponto no eixo Y
                self.historico.insert(END, f"e {sx} {sy}")
                self.scale_msg.config(text="Escalonamento adicionado ao histórico", foreground="SpringGreen2")
            except:
                self.scale_msg.config(text="Números Inválidos", foreground="Red")

        elif tab == "Rotação":
            try:
                var = self.option.get()
                if var == "p": #Rotação sobre um ponto
                    x = float(self.entrada_xp.get())
                    y = float(self.entrada_yp.get())
                    angulo = float(self.entrada_grau.get())
                    self.historico.insert(END, f"rp {x} {y} {angulo}")
                    self.point_msg.config(text="Rotação adicionado ao histórico", foreground="SpringGreen2")

                elif var == "o":    #Rotação sobre a origem
                    angulo = float(self.entrada_grau.get())
                    self.historico.insert(END, f"ro {angulo}")
                    self.general_msg.config(text="Rotação adicionado ao histórico", foreground="SpringGreen2")

                elif var == "s":    #Rotação sobre si mesmo
                    angulo = float(self.entrada_grau.get())
                    self.historico.insert(END, f"rs {angulo}")
                    self.general_msg.config(text="Rotação adicionado ao histórico", foreground="SpringGreen2")

                else:
                    self.general_msg.config(text="Selecione uma opção de rotação", foreground= "Red")
            except:
                self.general_msg.config(text="Valores Inválidos", foreground="Red")
                self.point_msg.config(text="Valores Inválidos", foreground="Red")
        else: 
            print("Erro a tab veio de forma errada")
    

    def calcular_mat(self):
        historico = self.historico.get(0,END)   #Recebe a listbox com as transformações ordenadas
        ant = np.matrix([[1,0,0], [0,1,0], [0,0,1]])    #Matriz identidade (valor simbolico de 1 na mult)
        objName = self.obj_trans    #Nome do objeto
        
        for items in historico:
            lista = items.split()
            match lista[0]:
                case "t": #Translacao
                    dx = float(lista[1])
                    dy = float(lista[2])
                    mat = self.transladar(dx,dy)
                    ant = np.matmul(ant,mat)    #Evolução da matriz de transformações
    
                case "e": #Escalonamento
                    sx = float(lista[1])    #Escalonamento por utilizar a relação do centro do objeto acaba aplicando a matriz de transformação
                    sy = float(lista[2])    # antes, nela é recalculado o centro do objeto, para dai então ser aplicado o escalonamento

                    self.obj_dict[self.obj_trans].moverXY(ant)
                    ant = np.matrix([[1,0,0], [0,1,0], [0,0,1]])

                    centrox = self.obj_dict[objName].centroX    #Novo centro do objeto X
                    centroy = self.obj_dict[objName].centroY    #Novo centro do objeto Y

                    mat1 = self.transladar(-centrox, -centroy)  #Leva o centro do objeto para a origem das coordenadas
                    ant = np.matmul(ant,mat1)
                    mat2 = self.escalonar(sx,sy)                #Escalona a matriz em relação a Sx e Sy
                    ant = np.matmul(ant,mat2)
                    mat3 = self.transladar(centrox, centroy)    #Devolve o centro do objeto até a posição original
                    ant = np.matmul(ant,mat3)

                case "ro": #Rotacao na origem
                    ang = float(lista[1])
                    mat = self.rotacionar(ang)                  #Simplesmente rotaciona em relação a origem
                    ant = np.matmul(ant,mat)

                case "rs": #Rotação pelo centro do obj

                    self.obj_dict[self.obj_trans].moverXY(ant)
                    ant = np.matrix([[1,0,0], [0,1,0], [0,0,1]])
                    
                    centrox = self.obj_dict[objName].centroX
                    centroy = self.obj_dict[objName].centroY

                    ang = float(lista[1])
                    mat1 = self.transladar(-(centrox), -(centroy))  #Leva o centro do objeto para a origem das coordenadas
                    ant = np.matmul(ant,mat1)
                    mat2 = self.rotacionar(ang)                     #Rotaciona a matriz pelo ângulo dado
                    ant = np.matmul(ant,mat2)
                    mat3 = self.transladar(centrox, centroy)        #Devolve o centro do objeto até a posição original
                    ant = np.matmul(ant,mat3)

                case "rp": #Rotação por um ponto
                    px = float(lista[1])
                    py = float(lista[2])
                    ang = float(lista[3])
                    mat1 = self.transladar(-px, -py)                #Leva o ponto para a origem das coordenadas
                    ant = np.matmul(ant,mat1)
                    mat2 = self.rotacionar(ang)                     #Rotaciona a matriz pelo ângulo dado
                    ant = np.matmul(ant,mat2)
                    mat3 = self.transladar(px, py)                  #Devolve o ponto até a posição original
                    ant = np.matmul(ant,mat3)
        return ant

    def transladar(self, dx, dy):
        return np.matrix([[1,0,0], [0,1,0], [dx,dy,1]])             #Devolve a matriz da translação

    def escalonar(self, sx, sy):
        return np.matrix([[sx,0,0], [0,sy,0], [0,0,1]])             #Devolve a matriz do escalonamento

    #np.sin(np.deg2rad(90))
    def rotacionar(self, ang):                                      #Devolve a matriz da rotação
        return np.matrix([[np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang)),  0], [-np.sin(np.deg2rad(ang)), np.cos(np.deg2rad(ang)), 0], [0,0,1]])

    def fim_trans(self):
        self.mat = self.calcular_mat()      #Calcula a matriz de transições
        self.historico.delete(0, END)
        self.obj_dict[self.obj_trans].moverXY(self.mat) #Proprio objeto aplica a matriz conforme sua especificidade
        mat = self.gerarDescricaoSCN()
        self.obj_dict[self.obj_trans].normalize(mat)
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
        mat1 = self.transladar(-self.windowObj.centroX, -self.windowObj.centroY) 
        mat2 = self.rotacionar(-self.windowObj.angulo)

        x = abs(self.windowObj.BE[0] - self.windowObj.BD[0])/2
        y = abs(self.windowObj.BE[1] - self.windowObj.CE[1])/2
        mat3 = self.escalonar(1/x, 1/y)
        result = np.matmul(mat1, mat2)
        result = np.matmul(result, mat3)
        return result
        

    #90 * np.pi/180

    def normalizar(self):
        mat = self.gerarDescricaoSCN()

        for obj in self.obj_dict.values():
            obj.normalize(mat)
        self.eixoY.normalize(mat)
        self.eixoX.normalize(mat)


    def rotacionarWin(self, ang):
        self.windowObj.angulo = (self.windowObj.angulo+ang % 360)
        self.normalizar()
        self.redesenhar()