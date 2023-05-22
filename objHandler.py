from tkinter import filedialog, simpledialog
from point import Point
from line import Line
from polygon import Polygon
from arame import Arame

class MTLReader:
    def __init__(self, name):
        self.colors = {}
        caminho = f"obj/{name}"
        with open(caminho, "r") as f:
            for line in f:
                if line.startswith("# "):
                    continue
                if line.startswith("newmtl "):
                    color_name = line.split()[1]
                if line.startswith("Kd "):
                    color_rgb = list(map(float, line.split()[1:]))
                    self.colors[color_name] = color_rgb
                else:
                    continue

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
            obj_name = ""
            grupo = []
            polygon = 0
            l = 0
            p = 0
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
                elif line.startswith("# "):
                    continue
                elif line.startswith("mtllib "):
                    self.matlib = MTLReader(line.split()[1])
                elif line.startswith("o ") or line.startswith("g "):
                    if self.objects != []:
                        if len(self.objects) == 1:                    #caso so tem um objeto guarda ele msm 
                            grupo.append(self.objects[0])
                        else:                                         #caso tenha mais objetos cria arame
                            arame = Arame(obj_name, self.objects)
                            grupo.append(arame)
                        self.objects = []
                    obj_name = line.split()[1]
                    #grupo_atual = obj_name
                elif line.startswith("usemtl "):
                    color = line.split()[1]
                    c = color.split(".")
                    if len(c) > 1:
                        color = c[0]
                elif line.startswith("p "):
                    v_index = list(map(int, line.split()[1:]))
                    if (v_index[0] > 0) :
                        point = [(self.vertices[v_index[0]-1][0], self.vertices[v_index[0]-1][1], self.vertices[v_index[0]-1][2])]
                    else:
                        point = [(self.vertices[v_index[0]][0], self.vertices[v_index[0]][1], self.vertices[v_index[0]][2])]

                    if obj_name == "":
                        obj_name = f"POINTDEFAULT{p}"
                    ponto = Point(obj_name, point)
                    p += 1
                    #obj_name = ""
                    if (color != ""):
                        r = int(self.matlib.colors[color][0] * 255)
                        g = int(self.matlib.colors[color][1] * 255)
                        b = int(self.matlib.colors[color][2] * 255)
                        color = ""
                        ponto.cor = self.rgb_to_hex(r,g,b)
                    self.objects.append(ponto)
        
                elif line.startswith("l ") or line.startswith("f "):    #depois face terá sua propria implementação com preenchimento 
                    v_index = list(line.split()[1:])

                    index = []
                    if "/" in str(v_index[0]):                              #caso seja f v/vt/vn v/vt/vn v/vt/vn
                        pontos = []
                        for vertexs in v_index:
                            v, *_ = vertexs.split('/')                  #pega apenas v
                            index.append(int(v))
                        for i in index:
                            pontos.append((self.vertices[i-1][0], self.vertices[i-1][1], self.vertices[i-1][2]))
                        if obj_name == "":                           #caso nao tem nome definido no .obj (exemplo do teapot)
                            obj_name = f"POLYGONDEFAULT{polygon}" 
                        poligono = Polygon(obj_name, pontos)
                        polygon += 1
                        if (color != ""):
                            r = int(self.matlib.colors[color][0] * 255)
                            g = int(self.matlib.colors[color][1] * 255)
                            b = int(self.matlib.colors[color][2] * 255)
                            color = ""
                            poligono.cor = self.rgb_to_hex(r,g,b)
                        self.objects.append(poligono)

                    elif len(v_index) > 2:                                #caso seja poligono 
                        #poligono
                        v_index = list(map(int, v_index))
                        pontos = []
                        if v_index[0] > 0:
                            for i in v_index:
                                pontos.append((self.vertices[i-1][0], self.vertices[i-1][1], self.vertices[i-1][2]))
                        else:
                            for i in v_index:
                                pontos.append((self.vertices[i][0], self.vertices[i][1], self.vertices[i][2]))
                        if obj_name == "":                           #caso nao tem nome definido no .obj (exemplo do teapot)
                            obj_name = f"POLYGONDEFAULT{polygon}" 
                        poligono = Polygon(obj_name, pontos)
                        polygon += 1
                        if (color != ""):
                            r = int(self.matlib.colors[color][0] * 255)
                            g = int(self.matlib.colors[color][1] * 255)
                            b = int(self.matlib.colors[color][2] * 255)
                            color = ""
                            poligono.cor = self.rgb_to_hex(r,g,b)
                        self.objects.append(poligono)

                    else:
                        #linha
                        v_index = list(map(int, v_index))
                        if v_index[0] > 0:
                            line = [(self.vertices[v_index[0]-1][0], self.vertices[v_index[0]-1][1], self.vertices[v_index[0]-1][2]),
                                    (self.vertices[v_index[1]-1][0], self.vertices[v_index[1]-1][1], self.vertices[v_index[1]-1][2])]
                        else:
                            line = [(self.vertices[v_index[0]][0], self.vertices[v_index[0]][1], self.vertices[v_index[0]][2]),
                                    (self.vertices[v_index[1]][0], self.vertices[v_index[1]][1], self.vertices[v_index[1]][2])]
                        if obj_name == "":
                            obj_name = f"LINEDEFAULT{l}"
                        linha = Line(obj_name, line)
                        l += 1
                        if (color != ""):
                            r = int(self.matlib.colors[color][0] * 255)
                            g = int(self.matlib.colors[color][1] * 255)
                            b = int(self.matlib.colors[color][2] * 255)
                            color = ""
                            linha.cor = self.rgb_to_hex(r,g,b)
                        self.objects.append(linha)
                
                if (not line):
                    if self.objects != []:
                        if len(self.objects) == 1:                    #caso so tem um objeto guarda ele msm 
                            grupo.append(self.objects[0])
                        else:                                         #caso tenha mais objetos cria arame
                            arame = Arame(obj_name, self.objects)
                            grupo.append(arame)
                    break
            return grupo


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
                    f.write(f"v {i[0]} {i[1]} {i[2]}\n")
            
                if (tipo == 1):                                 #ponto
                    f.write("p -1\n")
                elif (tipo == 2):                               #linha
                    f.write("l -2 -1\n")
                elif (tipo == 3):                               #poligono
                    f.write("l ")
                    for i in range(len(coord)):
                        num = (i*-1)-1
                        f.write(f"{num} ")
                    f.write(f"-1 {-len(coord)-1}")
                    f.write("\n")
                elif (tipo == 5):                               #curva
                    for i in range(len(coord),1,-1):
                        num = (i*-1)
                        if i != len(coord):
                            nome = f"LINECURVE{i+1}"
                            f.write(f"o {nome}\n")
                            f.write(f"usemtl {cor}\n")
                        f.write(f"l {num} {num+1}\n")
                elif (tipo == 7) or (tipo == 8):                #superficie
                    f.write(f"g {nome}\n")
                    f.write(f"usemtl {cor}\n")
                    for i in range(len(coord),1,-2):
                        num = (i*-1)
                        f.write(f"l {num} {num+1}\n")
                
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