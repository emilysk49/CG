'''
Não é parte do projeto, nem está em classe, só escrevemos rapidinho para que possamos utilizar os 
exemplos deixados no moodle na nossa versão do sistema mais simples
'''

with open("cristo.txt", "r") as f, open("teste.txt", "a") as f2:
    ii = 1
    f2.write("o 0\n")
    for line in f:
        if line.startswith("vt") or line.startswith("vn") or line.startswith("o ") or line.startswith("#"):
            continue
        elif line.startswith("f "):
            aa = []
            a = list(line.split()[1:])
            for i in a:
                aa.append(list(i.split("/")))
            
            a = "f " + aa[0][0] +" "+ aa[1][0] + " " + aa[2][0]
            f2.write(a+"\n")
            esc = ii
            f2.write("o " +str(esc)+"\n")
            ii += 1
        else:
            f2.write(line)
