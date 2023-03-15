from tkinter import *
from point import Point
from line import Line
from polygon import Polygon

#Verificar entradas se são int

class Window():
    def __init__(self):
        self.main_window = Tk()
        self.main_window.geometry("930x700+450+200")
        self.main_window.title("Computer Graphic")
        self.main_window["bg"]= "gray"

        #relief opcoes: solid, flat, raised, sunken
        self.dFile_frame = Frame(self.main_window, borderwidth=1, relief="raised", bg="gray")
        self.dFile_frame.place(x=10, y=10, width=200, height=670)

        #viewport
        self.canvas = Canvas(self.main_window, width=570, height=570, bg="floral white")
        self.canvas.place(x=230, y=10)
        
        #setando valores de window (da tela onde vai ter desenhos - viewport)
        self.xwMin = -10
        self.xwMax = 10
        self.ywMin = -10
        self.ywMax = 10

        #tamanho da tela do viewport
        self.xvMin = 0
        self.xvMax = 570
        self.yvMin = 0
        self.yvMax = 570

        #ainda nao tem implementacao e apenas frame
        self.log_frame = Frame(self.main_window, borderwidth=1, relief="raised", bg="gray")
        self.log_frame.place(x=230, y=600, width=570, height=80)

        #frame que terá objetos ja construidos
        self.scroll_frame = Frame(self.dFile_frame, bg="black")
        self.scroll_frame.place(x=170, y=20, height=120)
        self.objetos_text = Label(self.dFile_frame, text="Objetos", bg="gray")
        self.objetos_text.config(font =("Courier", 14), foreground="white")
        self.objetos_text.pack()
        self.scrollbar = Scrollbar(self.scroll_frame, orient=VERTICAL)
        self.object_list = Listbox(self.dFile_frame, width=17, height=7, bg="gray40", yscrollcommand=self.scrollbar.set)
        self.obj_dict = {}
        self.scrollbar.config(command=self.object_list.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.object_list.place(x=10, y=20)

        #botao para apagar objeto existente
        self.apagarB = Button(self.dFile_frame, text="Delete", command=lambda:self.apagar_objeto())
        self.apagarB.place(x=90, y=155)
        #botai para adicionar objeto novo -> vai para criacao de pop up
        self.objectB = Button(self.dFile_frame, text="Add", command=lambda:self.criar_objeto())
        self.objectB.place(x=10, y=155)

        #frame onde tera algumas funcoes para mexer 
        self.tool_frame = Frame(self.dFile_frame, relief="raised", borderwidth=1, bg="gray")
        self.tool_frame.place(x=10, y=200, width=170, height=450)

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
        self.linha1 = self.canvas.create_line(self.xvp(0), self.yvMax, self.xvp(0), self.yvMin, fill="gray", width=2, arrow=BOTH)
        self.linha2 = self.canvas.create_line(self.xvMin, self.yvp(0), self.xvMax, self.yvp(0), fill="gray", width=2, arrow=BOTH)

    #transformada de viewport x
    def xvp(self, xw):
        return ( ((xw-self.xwMin)/(self.xwMax - self.xwMin))*(self.xvMax-self.xvMin) ) 

    #transformada de viewport y
    def yvp(self, yw):
        return ( (1-((yw-self.ywMin)/(self.ywMax-self.ywMin)))*(self.yvMax-self.yvMin) )
    
    #para esquerda <- diminui os x
    def left(self):
        self.xwMin -= 1 
        self.xwMax -= 1
        self.redesenhar()

    #para direita -> aumenta os x
    def right(self):
        self.xwMax += 1
        self.xwMin += 1
        self.redesenhar()

    #para cima ↑ aumenta os y
    def up(self):
        self.ywMax += 1
        self.ywMin += 1
        self.redesenhar()

    #para baixo ↓ diminui os y
    def down(self):
        self.ywMax -= 1
        self.ywMin -= 1
        self.redesenhar()

    def zoomIn(self):
        #Verificacao para nao inverter a tela com muito zoomIn (rever para possiveis diferentes niveis de zoom)
        if not (((self.xwMax-1) <= (self.xwMin+1)) or ((self.yvMax-1) <= (self.yvMin+1))): 
            self.xwMax -= 1
            self.xwMin += 1
            self.ywMax -= 1
            self.ywMin += 1
        self.redesenhar()
        
    def zoomOut(self):
        self.xwMax += 1
        self.xwMin -= 1
        self.ywMax += 1
        self.ywMin -= 1
        self.redesenhar()

    def redesenhar(self):
        self.canvas.delete("all") #primeiro apaga tudo

        #vai verificar se tem objeto para redesenhar
        for obj in self.obj_dict.values():

            tup = obj.coordenadas
            
            if obj.tipo == 1: #se ponto
                self.canvas.create_oval(self.xvp(tup[0][0])-3, self.yvp(tup[0][1])-3, self.xvp(tup[0][0])+3, self.yvp(tup[0][1])+3, fill="red")

            elif obj.tipo == 2: #se linha
                self.canvas.create_line(self.xvp(tup[0][0]), self.yvp(tup[0][1]), self.xvp(tup[1][0]), self.yvp(tup[1][1]), fill="blue", width=3)
            
            elif obj.tipo == 3: #se poligono
                for i in range (len(tup)):
                    self.canvas.create_line(self.xvp(tup[i][0]), self.yvp(tup[i][1]), self.xvp(tup[i-1][0]), self.yvp(tup[i-1][1]), fill="purple3", width=3)
    
        #duas linhas eixo x e y para criar plano cartesiano
        self.linha1 = self.canvas.create_line(self.xvp(0), self.yvMax, self.xvp(0), self.yvMin, fill="gray", width=2, arrow=BOTH)
        self.linha2 = self.canvas.create_line(self.xvMin, self.yvp(0), self.xvMax, self.yvp(0), fill="gray", width=2, arrow=BOTH)

    def criar_ponto(self):
        try:
            nome = self.nome_obj.get()
            if not (nome in self.obj_dict.keys()): #verifica se nao tem o objeto com mesmo nome 
                x = float(self.entrada_x.get()) #cuida que x e y nao recebeu entrada de string
                y = float(self.entrada_y.get())
                self.object_list.insert(END, nome)
                self.obj_dict[nome] = Point(nome, [(x,y)])
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
                x1 = float(self.entrada_x1.get()) #cuida que x e y nao recebeu entrada de string
                y1 = float(self.entrada_y1.get())

                x2 = float(self.entrada_x2.get())
                y2 = float(self.entrada_y2.get())

                self.object_list.insert(END, nome)
                self.obj_dict[nome] = Line(nome, [(x1,y1),(x2,y2)])
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
            self.obj_dict[nome] = Polygon(nome, self.pontos_pol)
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


if __name__ == "__main__":
    app = Window()
    app.main_window.mainloop()