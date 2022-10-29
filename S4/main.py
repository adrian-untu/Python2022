import os
import sys

# 1)	Să se scrie o funcție ce primeste un singur parametru, director, ce reprezintă calea către un director.
# Funcția returnează o listă cu extensiile unice sortate crescator (in ordine alfabetica) a fișierelor din directorul dat ca parametru.
# Mențiune: extensia fișierului ‘fisier.txt’ este ‘txt’
def function1(director):
    try:
        return sorted(list(set([os.path.splitext(el)[1][1:] for el in os.listdir(director) if os.path.isfile(os.path.join(director,el)) and os.path.splitext(el)[1]!=""])))
    except Exception as e:
        print(str(e))
        return []

# 2)	Să se scrie o funcție ce primește ca argumente două căi: director si fișier.
# Implementati functia astfel încât în fișierul de la calea fișier să fie scrisă pe câte o linie,
# calea absolută a fiecărui fișier din interiorul directorului de la calea folder, ce incepe cu litera A.
def function2(director, fisier):
    try:
        with open(fisier,"w") as f:
            for el in os.listdir(director):
                name = os.path.join(director,el)
                if os.path.isfile(name) and el.startswith("A"):
                    print(repr(os.path.abspath(name)+os.linesep))
                    f.write(os.path.abspath(name)+os.linesep)
    except Exception as e:
        print(str(e))

# 3) Să se scrie o funcție ce primește ca parametru un string my_path.
# Dacă parametrul reprezintă calea către un fișier, se vor returna ultimele
# 20 de caractere din conținutul fișierului. Dacă parametrul reprezintă calea către un director,
# se va returna o listă de tuple (extensie, count), sortată descrescător după count,
# unde extensie reprezintă extensie de fișier, iar count - numărul de fișiere cu acea extensie.
# Lista se obține din toate fișierele (recursiv) din directorul dat ca parametru.
def function3(my_path):
    if os.path.isfile(my_path):
        with open(my_path,"rb") as f:
            file_size = os.path.getsize(my_path)
            assert(file_size>=20),"File needs to have min 20 characters"
            f.seek(file_size-20)
            return f.read()
    elif os.path.isdir(my_path):
        lista = {}
        for root, dirs, files in os.walk(my_path):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in lista:
                    lista[ext] += 1
                else:
                    lista[ext] = 1
        lista = lista.items()
        return sorted(lista,key=lambda el:el[1],reverse=True)
    else:
        raise Exception("Invalid parameter.")

# 4)	Să se scrie o funcție ce returnează o listă cu extensiile unice a fișierelor din directorul dat
# ca argument la linia de comandă (nerecursiv). Lista trebuie să fie sortată crescător.
# Mențiune: extensia fișierului ‘fisier.txt’ este ‘txt’, iar ‘fisier’ nu are extensie, deci nu va apărea în lista finală.
def function4():
    try:
        assert(len(sys.argv)>1),"Invalid number of parameters"
        assert(os.path.isdir(sys.argv[1])),"Invalid director"
        return sorted(list(set([os.path.splitext(el)[1][1:] for el in os.listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1],el)) and os.path.splitext(el)[1]!=""])))
    except Exception as e:
        print(str(e))
        return []

# 5)	Să se scrie o funcție care primește ca argumente două șiruri de caractere,
# target și to_search și returneaza o listă de fișiere care conțin to_search.
# Fișierele se vor căuta astfel: dacă target este un fișier, se caută doar in fișierul
# respectiv iar dacă este un director se va căuta recursiv in toate fișierele din acel director.
# Dacă target nu este nici fișier, nici director, se va arunca o excepție de tipul ValueError cu un mesaj corespunzator.
def function5(target,to_search):
    def file_contains_to_search(target, to_search):
        with open(target,"rt") as f:
            text = f.read()
            return to_search in text

    if (os.path.isfile(target)):
        if file_contains_to_search(target,to_search):
            return [target]
        else:
            return []
    elif(os.path.isdir(target)):
        result = []
        for root,dirs,files in os.walk(target):
            for f in files:
                name = os.path.join(root,f)
                if file_contains_to_search(name,to_search):
                   result+=[name]
        return result
    else:
        raise ValueError("Target needs to be file/directory")

# 6)	Să se scrie o funcție care are același comportament ca funcția de la exercițiul anterior,
# cu diferența că primește un parametru în plus: o funcție callback, care primește un parametru,
# iar pentru fiecare eroare apărută în procesarea fișierelor,
# se va apela funcția respectivă cu instanța excepției ca parametru.
def function6(target, to_search, callback):
    try:
        return function5(target,to_search)
    except Exception as e:
        callback(e)
        return []

# 7)	Să se scrie o funcție care primește ca parametru un șir de caractere care reprezintă calea
# către un fișer si returnează un dicționar cu următoarele cămpuri: full_path = calea absoluta catre fisier,
# file_size = dimensiunea fisierului in octeti, file_extension = extensia fisierului (daca are) sau "",
# can_read, can_write = True/False daca se poate citi din/scrie in fisier.
def function7(fisier):
    try:
        assert(os.path.isfile(fisier)),"The parameter needs to be a file path"
        return {"full_path":os.path.abspath(fisier),
                "file_size":os.path.getsize(fisier),
                "file_extension":os.path.splitext(fisier)[1],
                "can_read":os.access(fisier,os.R_OK),
                "can_write":os.access(fisier,os.W_OK)}
    except Exception as e:
        print(str(e))
        return {}

# 8)	Să se scrie o funcție ce primește un parametru cu numele dir_path. Acest parametru reprezintă calea către un director aflat pe disc.
# Funcția va returna o listă cu toate căile absolute ale fișierelor aflate în rădăcina directorului dir_path.
# Exemplu apel funcție: functie("C:\\director") va returna ["C:\\director\\fisier1.txt", "C:\\director\\fisier2.txt"]
def function8(dir_path):
    try:
        result = []
        for el in os.listdir(dir_path):
            if(os.path.isfile(el)):
                name = os.path.join(dir_path,el)
                result+=[os.path.abspath(name)]
        return result
    except Exception as e:
        print(str(e))
        return []

#print all results of functions:
if __name__ == '__main__':
    print("PROBLEM 1:\n" + str(function1("D:\Facultate anul 3\PP (Programare in Python)\Python2022\S4")))
    print("PROBLEM 2:\n" + str(function2("D:\Facultate anul 3\PP (Programare in Python)\Python2022\S4", "a.txt")))
    print("PROBLEM 3:\n" + str(function3("D:\Facultate anul 3\PP (Programare in Python)\Python2022\S4\main.py")))
    print("PROBLEM 4:\n" + str(function4())) # file given as path in the configuration of the script
    print("PROBLEM 5:\n" + str(function5("D:\Facultate anul 3\PP (Programare in Python)\Python2022\S4", "D:\Facultate anul 3\PP (Programare in Python)\Python2022\S4")))
    print("PROBLEM 6:\n" + str(function6("D:\Facultate anul 3\PP (Programare in Python)\Python2022\S4", "D:\Facultate anul 3\PP (Programare in Python)\Python2022\S4", callback="D:\Facultate anul 3\PP (Programare in Python)\Python2022\S4")))
    print("PROBLEM 7:\n" + str(function7("main.py")))
    print("PROBLEM 8:\n" + str(function8("D:\Facultate anul 3\PP (Programare in Python)\Python2022\S4")))