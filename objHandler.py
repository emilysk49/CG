from tkinter import filedialog, simpledialog
from point import Point
from line import Line
from polygon import Polygon

class MTLReader:
    def __init__(self, name):
        self.colors = {}

        with open(name, "r") as f:
            for line in f:
                if line.startswith("newmtl "):
                    color_name = line.split()[1]
                if line.startswith("Kd "):
                    color_rgb = list(map(float, line.split()[1:]))
                    self.colors[color_name] = color_rgb

class ObjHandler:
    def __init__(self):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.objects = []
        self.matlib = str
        
        
    def open_file(self):
        
        file_path = filedialog.askopenfilename()
        with open(file_path, "r") as f:
            color = ""
            while True:
                line = f.readline()
                if line.startswith("v "):
                    vertex = list(map(float, line.split()[1:]))
                    self.vertices.append(vertex)
                elif line.startswith("vn "):
                    normal = list(map(float, line.split()[1:]))
                    self.normals.append(normal)
                elif line.startswith("vt "):
                    texcoord = list(map(float, line.split()[1:]))
                    self.texcoords.append(texcoord)
                #elif line.startswith("f "):
                #    face = []
                #    for vertex_desc in line.split()[1:]:
                #        indices = [int(index) if index else 0 for index in vertex_desc.split("/")]
                #        face.append(indices)
                #    self.faces.append(face)
                elif line.startswith("mtllib "):
                    self.matlib = MTLReader(line.split()[1])
                elif line.startswith("o ") or line.startswith("g "):
                    obj_name = line.split()[1]
                elif line.startswith("usemtl "):
                    color = line.split()[1]
                elif line.startswith("p "):
                    v_index = list(map(int, line.split()[1:]))
                    if (v_index[0] > 0) :
                        point = [(self.vertices[v_index[0]-1][0], self.vertices[v_index[0]-1][1])]
                    else:
                        point = [(self.vertices[v_index[0]][0], self.vertices[v_index[0]][1])]
                    ponto = Point(obj_name, point)
                    obj_name = ""
                    if (color != ""):
                        r = int(self.matlib.colors[color][0] * 255)
                        g = int(self.matlib.colors[color][1] * 255)
                        b = int(self.matlib.colors[color][2] * 255)
                        color = ""
                        ponto.cor = self.rgb_to_hex(r,g,b)
                    self.objects.append(ponto)
        
                elif line.startswith("l ") or line.startswith("f "):    #depois face terá sua propria implementação com preenchimento 
                    v_index = list(map(int, line.split()[1:]))
                    if len(v_index) > 2:
                        #poligono
                        pontos = []
                        if v_index[0] > 0:
                            for i in v_index:
                                pontos.append((self.vertices[i-1][0], self.vertices[i-1][1]))
                        else:
                            for i in v_index:
                                pontos.append((self.vertices[i][0], self.vertices[i][1]))
                        poligono = Polygon(obj_name, pontos)
                        obj_name = ""
                        if (color != ""):
                            r = int(self.matlib.colors[color][0] * 255)
                            g = int(self.matlib.colors[color][1] * 255)
                            b = int(self.matlib.colors[color][2] * 255)
                            color = ""
                            poligono.cor = self.rgb_to_hex(r,g,b)
                        self.objects.append(poligono)
                    else:
                        #linha
                        if v_index[0] > 0:
                            line = [(self.vertices[v_index[0]-1][0], self.vertices[v_index[0]-1][1]),
                                    (self.vertices[v_index[1]-1][0], self.vertices[v_index[1]-1][1])]
                        else:
                            line = [(self.vertices[v_index[0]][0], self.vertices[v_index[0]][1]),
                                    (self.vertices[v_index[1]][0], self.vertices[v_index[1]][1])]
                        linha = Line(obj_name, line)
                        obj_name = ""
                        if (color != ""):
                            r = int(self.matlib.colors[color][0] * 255)
                            g = int(self.matlib.colors[color][1] * 255)
                            b = int(self.matlib.colors[color][2] * 255)
                            color = ""
                            linha.cor = self.rgb_to_hex(r,g,b)
                        self.objects.append(linha)
                
                if (not line):
                    break

            return self.objects


    def write_file(self, dict_list):
        file_name = simpledialog.askstring(title="Savefile", prompt="Digite nome do arquivo")
        colors = set()                          #Set para não escrevermos duas vezes caso algum objeto tenha a mesma cor que outro
        with open(file_name+".obj", "a") as f:
            f.write(f"mtllib {file_name}.mtl\n")
            for obj in dict_list:
                nome = obj["nome"]
                coord = obj["coord"]
                cor = obj["cor"]
                tipo = obj["tipo"]
                colors.add(cor)

                f.write(f"o {nome}\n")
                f.write(f"usemtl {cor}\n")
                for i in coord:
                    f.write(f"v {i[0]} {i[1]} 0\n")
            
                if (tipo == 1):
                    f.write("p -1\n")
                elif (tipo == 2):
                    f.write("l -2 -1\n")
                else:
                    f.write("l ")
                    for i in range(len(coord)):
                        num = (i*-1)-1
                        f.write(f"{num} ")
                    f.write("\n")

        with open(file_name+".mtl", "a") as f:
            for c in colors:
                f.write(f"newmtl {c}\n")
                (r,g,b) = self.hex_to_rgb(c)
                f.write(f"Kd {r} {g} {b}\n")


    #https://www.educative.io/answers/how-to-convert-hex-to-rgb-and-rgb-to-hex-in-python
    def rgb_to_hex(self, r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def hex_to_rgb(self, hex_value):
        hex_value = hex_value.lstrip('#') # remove o caractere '#' da string, se existir
        r, g, b = tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
        return r/255, g/255, b/255