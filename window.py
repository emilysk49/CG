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
        self.dFile_frame = Frame(self.main_window, borderwidth=1, relief="raised", bg="gray")
        #relief opcoes: solid, flat, raised, sunken
        self.dFile_frame.place(x=10, y=10, width=200, height=670)

        self.canvas = Canvas(self.main_window, width=570, height=570, bg="floral white")
        self.canvas.place(x=230, y=10)
        
        self.xwMin = -10
        self.xwMax = 10
        self.ywMin = -10
        self.ywMax = 10

        self.xvMin = 0
        self.xvMax = 570
        self.yvMin = 0
        self.yvMax = 570

        self.log_frame = Frame(self.main_window, borderwidth=1, relief="raised", bg="gray")
        self.log_frame.place(x=230, y=600, width=570, height=80)

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

        self.apagarB = Button(self.dFile_frame, text="Delete", command=lambda:self.apagar_objeto())
        self.apagarB.place(x=90, y=155)
        self.objectB = Button(self.dFile_frame, text="Add", command=lambda:self.criar_objeto())
        self.objectB.place(x=10, y=155)

        self.tool_frame = Frame(self.dFile_frame, relief="raised", borderwidth=1, bg="gray")
        self.tool_frame.place(x=10, y=200, width=170, height=450)

        self.linha1 = self.canvas.create_line(self.xvp(0), self.yvMax, self.xvp(0), self.yvMin, fill="gray", width=2, arrow=BOTH)
        self.linha2 = self.canvas.create_line(self.xvMin, self.yvp(0), self.xvMax, self.yvp(0), fill="gray", width=2, arrow=BOTH)
        #self.linha3 = self.canvas.create_line(self.xvp(2), self.yvp(3), self.xvp(8), self.yvp(-9), fill="blue", width=3)

        self.upB = Button(self.tool_frame, text="UP", width=5, command=lambda:self.up())
        self.upB.place(x=50, y=15)
        self.leftB = Button(self.tool_frame, text="LEFT", width=5, command=lambda:self.left())
        self.leftB.place(x=18, y=45)
        self.rightB = Button(self.tool_frame, text="RIGHT", width=5, command=lambda:self.right())
        self.rightB.place(x=85, y=45)
        self.downB = Button(self.tool_frame, text="DOWN", width=5, command=lambda:self.down())
        self.downB.place(x=50, y=75)

        self.zoominB = Button(self.tool_frame, text="+", width=3, command=lambda:self.zoomIn())
        self.zoominB.place(x=19, y=120)
        self.zoomoutB = Button(self.tool_frame, text="-", width=3, command=lambda:self.zoomOut())
        self.zoomoutB.place(x=100, y=120)

        self.ponto = None


    def xvp(self, xw):
        return ( ((xw-self.xwMin)/(self.xwMax - self.xwMin))*(self.xvMax-self.xvMin) ) # 18/20 * 570

    def yvp(self, yw):
        return ( (1-((yw-self.ywMin)/(self.ywMax-self.ywMin)))*(self.yvMax-self.yvMin) ) # (1-(/20)) * 570
    
    def apagar_objeto(self):
        for linha in self.object_list.curselection():
            del self.obj_dict[self.object_list.get(linha)]
            self.object_list.delete(linha)
        self.redesenhar()


    def levantar_frame(self, frame:Frame):
        self.pontos_pol = [] #Ao trocar para outra entrada perde-se o progresso
        frame.tkraise()

    def criar_ponto(self):
        try:
            #por enquanto permite 2 com mesmo nome (vai dar erros)
            nome = self.nome_obj.get()
            if not (nome in self.obj_dict.keys()):
                x = float(self.entrada_x.get())
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
            if not (nome in self.obj_dict.keys()):
                x1 = float(self.entrada_x1.get())
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

    def criar_poligono(self):
        nome = self.nome_obj3.get()
        if not (nome in self.obj_dict.keys()):
            self.object_list.insert(END, nome)
            self.obj_dict[nome] = Polygon(nome, self.pontos_pol)
            self.redesenhar()
            self.msg_label3.config(text="Polígono criado!", foreground="SpringGreen2")
        else:
            self.msg_label3.config(text="Nome já existente!", foreground="red")

    def add_ponto_pol(self):
        try:
            x = float(self.entrada_x3.get())
            y = float(self.entrada_y3.get())
            self.pontos_pol.append((x,y))
            self.msg_label3.config(text="Ponto adicionado!", foreground="SpringGreen2")
        except:
            self.msg_label3.config(text="Apenas números!", foreground="red")

    def redesenhar(self):
        self.canvas.delete("all")

        for obj in self.obj_dict.values():

            tup = obj.coordenadas
            
            if obj.tipo == 1:
                self.canvas.create_oval(self.xvp(tup[0][0])-3, self.yvp(tup[0][1])-3, self.xvp(tup[0][0])+3, self.yvp(tup[0][1])+3, fill="red")

            elif obj.tipo == 2:
                self.canvas.create_line(self.xvp(tup[0][0]), self.yvp(tup[0][1]), self.xvp(tup[1][0]), self.yvp(tup[1][1]), fill="blue", width=3)
            
            elif obj.tipo == 3:
                for i in range (len(tup)):
                    self.canvas.create_line(self.xvp(tup[i][0]), self.yvp(tup[i][1]), self.xvp(tup[i-1][0]), self.yvp(tup[i-1][1]), fill="purple3", width=3)
                    

        #linhas de plano cartesiano
        self.linha1 = self.canvas.create_line(self.xvp(0), self.yvMax, self.xvp(0), self.yvMin, fill="gray", width=2, arrow=BOTH)
        self.linha2 = self.canvas.create_line(self.xvMin, self.yvp(0), self.xvMax, self.yvp(0), fill="gray", width=2, arrow=BOTH)


    def left(self):
        self.xwMin -= 1
        self.xwMax -= 1
        self.redesenhar()

    def right(self):
        self.xwMax += 1
        self.xwMin += 1
        self.redesenhar()

    def up(self):
        self.ywMax += 1
        self.ywMin += 1
        self.redesenhar()

    def down(self):
        self.ywMax -= 1
        self.ywMin -= 1
        self.redesenhar()

    #Verificacao para nao inverter a tela com muito zoomIn (rever para possiveis diferentes niveis de zoom)
    def zoomIn(self):
        if not (((self.xwMax-1) <= (self.xwMin+1)) or ((self.yvMax-1) <= (self.yvMin+1))): 
            self.ywMax -= 1
            self.ywMin += 1
            self.xwMax -= 1
            self.xwMin += 1
        self.redesenhar()
        
    def zoomOut(self):
        self.ywMax += 1
        self.ywMin -= 1
        self.xwMax += 1
        self.xwMin -= 1
        self.redesenhar()

    def criar_objeto(self):
        #global pop
        self.pop = Toplevel(self.main_window)
        self.pop.geometry("300x300+450+200")
        self.pop.title("Create New Object")
        self.pop.config(bg="gray")

        #frame ponto pop up
        self.point_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.point_frame.place(x=100, y=0) 
        self.nome_label = Label(self.point_frame, bg="gray", text="Nome :")
        self.nome_label.place(x=5, y=5)
        self.nome_obj = Entry(self.point_frame, width=12)
        self.nome_obj.place(x=52, y=5)
        self.x_label = Label(self.point_frame, bg="gray", text="X :")
        self.x_label.place(x=5, y=50)
        self.entrada_x = Entry(self.point_frame, width=5)
        self.entrada_x.place(x=25, y=50)
        self.y_label = Label(self.point_frame, bg="gray", text="Y :")
        self.y_label.place(x=100, y=50)
        self.entrada_y = Entry(self.point_frame, width=5)
        self.entrada_y.place(x=120, y=50)
        self.concluirB = Button(self.point_frame, text="CONCLUIR", command=lambda:self.criar_ponto())
        self.concluirB.place(x=50, y=100)
        self.msg_label = Label(self.point_frame, text="", bg="gray")
        self.msg_label.place(x=10, y=150)

        #frame linha pop up
        self.line_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.line_frame.place(x=100, y=0) 
        self.nome_label = Label(self.line_frame, bg="gray", text="Nome :")
        self.nome_label.place(x=5, y=5)
        self.nome_obj2 = Entry(self.line_frame, width=12)
        self.nome_obj2.place(x=52, y=5)
        self.x_label = Label(self.line_frame, bg="gray", text="X1 :")
        self.x_label.place(x=5, y=50)
        self.entrada_x1 = Entry(self.line_frame, width=5)
        self.entrada_x1.place(x=32, y=50)
        self.y_label = Label(self.line_frame, bg="gray", text="Y1 :")
        self.y_label.place(x=100, y=50)
        self.entrada_y1 = Entry(self.line_frame, width=5)
        self.entrada_y1.place(x=127, y=50)
        self.x2_label = Label(self.line_frame, bg="gray", text="X2 :")
        self.x2_label.place(x=5, y=80)
        self.entrada_x2 = Entry(self.line_frame, width=5)
        self.entrada_x2.place(x=32, y=80)
        self.y2_label = Label(self.line_frame, bg="gray", text="Y2 :")
        self.y2_label.place(x=100, y=80)
        self.entrada_y2 = Entry(self.line_frame, width=5)
        self.entrada_y2.place(x=127, y=80)
        self.concluirB = Button(self.line_frame, text="CONCLUIR", command=lambda:self.criar_linha())
        self.concluirB.place(x=50, y=150)
        self.msg_label2 = Label(self.line_frame, text="", bg="gray")
        self.msg_label2.place(x=10, y=180)

        #frame poligono pop up
        self.polygon_frame = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.polygon_frame.place(x=100, y=0) 
        self.nome_label = Label(self.polygon_frame, bg="gray", text="Nome :")
        self.nome_label.place(x=5, y=5)
        self.nome_obj3 = Entry(self.polygon_frame, width=12)
        self.nome_obj3.place(x=52, y=5)
        self.x_label = Label(self.polygon_frame, bg="gray", text="X :")
        self.x_label.place(x=5, y=50)
        self.entrada_x3 = Entry(self.polygon_frame, width=5)
        self.entrada_x3.place(x=25, y=50)
        self.y_label = Label(self.polygon_frame, bg="gray", text="Y :")
        self.y_label.place(x=100, y=50)
        self.entrada_y3 = Entry(self.polygon_frame, width=5)
        self.entrada_y3.place(x=120, y=50)
        self.addB = Button(self.polygon_frame, text="ADICIONAR", command=lambda:self.add_ponto_pol())
        self.addB.place(x=0, y=100)
        self.concluirB = Button(self.polygon_frame, text="CONCLUIR", command=lambda:self.criar_poligono())
        self.concluirB.place(x=100, y=100)
        self.msg_label3 = Label(self.polygon_frame, text="", bg="gray")
        self.msg_label3.place(x=10, y=150)

        #Janela pop-up
        self.pop_padrao = Frame(self.pop, bg="gray", borderwidth=1, relief="raised", width=200, height=300)
        self.pop_padrao.place(x=100, y=0) 
        self.msg = Label(self.pop_padrao, text="Selecione objeto que \n quer desenhar!", bg="gray")
        self.msg.place(x=30, y=120)

        #Botoes para selecionar qual objeto adicionar
        self.pointB = Button(self.pop, text="Point", width=5, command=lambda:self.levantar_frame(self.point_frame))
        self.pointB.place(x=10, y=10)
        self.lineB = Button(self.pop, text="Line", width=5, command=lambda:self.levantar_frame(self.line_frame))
        self.lineB.place(x=10, y=40)
        self.polygonB = Button(self.pop, text="Polygon", width=5, command=lambda:self.levantar_frame(self.polygon_frame))
        self.polygonB.place(x=10, y=70)


if __name__ == "__main__":
    app = Window()
    app.main_window.mainloop()