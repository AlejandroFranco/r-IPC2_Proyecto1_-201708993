import copy
import re
from pip._vendor.distlib.compat import raw_input
import xml.etree.ElementTree as ET
import os

class Vertice:
    def __init__(self, i, h=0):
        self.id = i
        self.heuristica = h
        self.vecinos = []
        self.visitado = False
        self.padre = None
        self.costo = float('inf')
        self.costoF = float('inf')

    def agregarVecino(self, v, p):
        if v not in self.vecinos:
            self.vecinos.append([v, p])


class Grafica:

    def __init__(self):

        self.vertices = {}

    # h es la heuristica
    def agregarVertice(self, id, h=0):
        if id not in self.vertices:
            self.vertices[id] = Vertice(id, h)

    #donde p es el peso
    def agregarArista(self, a, b, p):

        if a in self.vertices and b in self.vertices:
            self.vertices[a].agregarVecino(b, p)
            self.vertices[b].agregarVecino(a, p)

    def imprimirGrafica(self):
        for v in self.vertices:
            print("El costo del vértice " + str(self.vertices[v].id) + " con heuristica " + str(
                self.vertices[v].heuristica) + " es " + str(self.vertices[v].costo) + " llegando desde " + str(
                self.vertices[v].padre))

    def camino(self, a, b):
        camino = []
        actual = b
        while actual is not None:
            camino.insert(0, actual)
            actual = self.vertices[actual].padre
        return camino

    def minimoH(self, l):
        if len(l) > 0:
            m = self.vertices[l[0]].costoF
            v = l[0]
            for e in l:
                if m > self.vertices[e].costoF:
                    m = self.vertices[e].costoF
                    v = e
            return v

    def aEstrella(self, a, b):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].costo = 0
            self.vertices[a].costoF = self.vertices[a].heuristica

        for v in self.vertices:
            if v != a:
                self.vertices[v].costo = float('inf')
                self.vertices[v].costoF = float('inf')
            self.vertices[v].padre = None

        abierto = [a]

        while len(abierto) > 0:
            actual = self.minimoH(abierto)
            if actual == b:
                return self.camino(a, b)
            abierto.remove(actual)
            self.vertices[actual].visitado = True

            for v in self.vertices[actual].vecinos:
                if not self.vertices[v[0]].visitado:
                    if self.vertices[v[0]].id not in abierto:
                        abierto.append(v[0])
                    if self.vertices[actual].costo + v[1] < self.vertices[v[0]].costo:
                        self.vertices[v[0]].padre = actual
                        self.vertices[v[0]].costo = self.vertices[actual].costo + v[1]
                        self.vertices[v[0]].costoF = self.vertices[v[0]].costo + self.vertices[v[0]].heuristica


class Casilla:
    def __init__(self, x, y, valor, siguiente=None):
        self.x = x
        self.y = y
        self.valor = valor
        self.siguiente = siguiente

class Fila:
    def __init__(self, casilla=None, siguiente=None):
        self.casilla = casilla
        self.siguiente = siguiente

    def append(self, x, y, valor):
        if self.casilla is None:
            self.casilla = Casilla(x, y, valor, None)
            return
        iterador = self.casilla
        while iterador.siguiente:
            iterador = iterador.siguiente
        iterador.siguiente = Casilla(x, y, valor, None)


class Matriz:
    def __init__(self, fila=None, siguiente=None):
        self.fila = fila
        self.siguiente = siguiente

    #insertar al final
    def append(self, fila):
        if self.fila is None:
            self.fila = Fila(fila.casilla, fila.siguiente)
            return
        iterador = self.fila
        while iterador.siguiente:
            iterador = iterador.siguiente
        iterador.siguiente = Fila(fila.casilla, fila.siguiente)

class Terreno:
    def __init__(self, nombre, xini, yini, xf, yf, matriz):
        self.nombre = nombre
        self.xini = xini
        self.yini = yini
        self.xf = xf
        self.yf = yf
        self.matriz = matriz

class Nodo:
    def __init__(self, datos=None, siguiente=None):
        self.datos = datos
        self.siguiente = siguiente

class LinkedList:
    def __init__(self):
        self.cabeza = None

    #insertar al principio
    def preppend(self, datos):
        nodo = Nodo(datos, self.cabeza)
        self.cabeza = nodo

    #insertar al final
    def append(self, datos):
        if self.cabeza is None:
            self.cabeza = Nodo(datos, None)
            return
        iterador = self.cabeza
        while iterador.siguiente:
            iterador = iterador.siguiente
        iterador.siguiente = Nodo(datos, None)

    def get_length(self):
        contador = 0
        iterador = self.cabeza
        while iterador:
            contador += 1
            iterador = iterador.siguiente
        return contador

    def eliminar_pos(self, indice):
        if indice < 0 or indice > self.get_length():
            raise Exception("Indice invalido")
        if indice == 0:
            self.cabeza = self.cabeza.siguiente
            return
        conteo = 0
        iterador = self.cabeza
        while iterador:
            if conteo == indice -1:
                iterador.siguiente = iterador.siguiente.siguiente
                break
            iterador = iterador.siguiente
            conteo += 1

    def insertar_pos(self, indice, datos):
        if indice < 0 or indice > self.get_length():
            raise Exception("Indice invalido")
        if indice == 0:
            self.preppend(datos)
            return
        contador = 0
        iterador = self.cabeza
        while iterador:
            if contador == indice -1:
                nodo = Nodo(datos,  iterador.siguiente)
                iterador.siguiente = nodo
                break

            iterador = iterador.siguiente
            contador += 1


class Main:

    lista_terrenos = LinkedList()

    def menu(self):
        print("\n")
        print("1 Cargar archivo")
        print("2 Procesar archivo")
        print("3 Escribir archivo de salida")
        print("4 Mostrar datos del estudiante")
        print("5 Generar gráfica")
        print("6 salida" + "\n")
        entrada = input("Ingrese un numero 1-6" + "\n")
        patron = "[1-6]{1}"
        if re.search(patron, entrada):
            if entrada == "1":
                self.cargarArchivo()
                self.menu()
            elif entrada == "2":
               self.procesarArchivo()
               self.menu()
            elif entrada == "3":
                a = 1
            elif entrada == "4":
               self.mostrarDatos()
            elif entrada == "5":
                self.generarGrafica()
                self.menu()
            elif entrada == "6":
                raw_input("Presione una tecla" + "\n")
        else:
            self.menu()

    def generarGrafica(self):
        contenido = ""
        iterador = self.lista_terrenos.cabeza
        while iterador:
            print(iterador.datos.nombre)
            iterador = iterador.siguiente
        terreno_graficar = input("Ingrese el nombre del terreno")
        terreno_seleccionado = None
        iterador = self.lista_terrenos.cabeza
        while iterador:
            if iterador.datos.nombre == terreno_graficar:
                terreno_seleccionado = iterador
                break
            iterador = iterador.siguiente

        fila = terreno_seleccionado.datos.matriz.fila
        contenido += "digraph "+terreno_graficar + "{" + "\n"
        contenido += "node  [shape=plaintext]"+"\n"
        contenido += "splines=line"+"\n"
        contenido += "struct1 [label=<"+"\n"
        contenido += "<TABLE BORDER=" + "\""+"0"+"\"" + "CELLBORDER=" + "\"" + "1" + "\"" + " CELLSPACING=" + "\"" + "20" + "\"" + " CELLPADDING=" + "\"" + "10"+"\"" + ">"+"\n"
        contenido += "<tr>"+"\n"
        contador_puerto = 0
        contador_struct = 1
        while fila:
            if fila is not None:
                if contador_struct > 1:
                    contenido += "</TR>"+"\n"
                    contenido += "</TABLE >>];"+"\n"
                    contenido +="\n"
                    contenido += "struct" + str(contador_struct) + "[label=<" + "\n"
                    contenido += "<TABLE BORDER=" + "\"" + "0" + "\"" + "CELLBORDER=" + "\"" + "1" + "\"" + " CELLSPACING=" + "\"" + "20" + "\"" + " CELLPADDING=" + "\"" + "10" + "\"" + ">" + "\n"
                    contenido += "<tr>" + "\n"
                casilla = fila.casilla
                while casilla:
                    if casilla is not None:
                        contenido += "<TD PORT "+"f" + str(contador_puerto)+">" + str(casilla.valor)+"</TD>"+"\n"
                        contador_puerto += 1
                    else:
                        break
                    casilla = casilla.siguiente
            else:
                break
            fila = fila.siguiente
            contador_struct += 1
        contenido += "</TR>" + "\n"
        contenido += "</TABLE >>];" + "\n"
        #contenido += "\n"+"}"
        file = open("grafico.dot", "w+")
        file.write(contenido)
        file.close()
        #os.system('cmd /k "dot -Tpng grafico.dot -o grafico.png"')
        #os.system('cmd /k "grafico.png"')

    def cargarArchivo(self):
        nombre_archivo = input("Ingrese la ruta del archivo")
        if os.path.exists(nombre_archivo) and nombre_archivo.endswith(".xml", len(nombre_archivo)-4, len(nombre_archivo)):
                arbol = ET.parse(nombre_archivo)
                raiz = arbol.getroot()
                lista_casillas = Fila()
                matriz = Matriz()
                terrenos = raiz.findall('terreno')
                for terreno in terrenos:
                    nombre_terreno = terreno.attrib['nombre']
                    xini = terreno.find('posicioninicio/x').text
                    yini = terreno.find('posicioninicio/y').text
                    xf = terreno.find('posicionfin/x').text
                    yf = terreno.find('posicionfin/y').text
                    contador = 1
                    posiciones = terreno.findall('posicion')
                    for posicion in posiciones:
                        valor = posicion.text
                        coordx = posicion.attrib['x']
                        coordy = posicion.attrib['y']
                        if posicion.attrib['x'] == str(contador):
                            lista_casillas.append(coordx, coordy, valor)
                        else:
                            matriz.append(lista_casillas)
                            lista_casillas = Fila()
                            contador += 1
                            lista_casillas.append(coordx, coordy, valor)
                    matriz.append(lista_casillas)
                    lista_casillas = Fila()
                    self.lista_terrenos.append(Terreno(nombre_terreno, xini, yini, xf, yf, matriz))
                    matriz = Matriz()
        else:
            print("Ingrese una ruta valida")
            self.cargarArchivo()


    def procesarArchivo(self):
        iterador = self.lista_terrenos.cabeza
        while iterador:
            print(iterador.datos.nombre)
            iterador = iterador.siguiente
        terreno_procesar = input("ingrese el nombre del terreno a procesar")
        terreno_elegido = None
        iterador = self.lista_terrenos.cabeza
        while iterador:
            if iterador.datos.nombre == terreno_procesar:
                terreno_elegido = iterador
                break
            iterador = iterador.siguiente

        #creo los vertices de la gráfica
        grafica = Grafica()
        fila = terreno_elegido.datos.matriz.fila
        while fila:
            if fila is not None:
                casilla = fila.casilla
                while casilla:
                    if casilla is not None:
                        grafica.agregarVertice(casilla.x + "," + casilla.y, 0)
                    else:
                        break
                    casilla = casilla.siguiente
            else:
                break
            fila = fila.siguiente
        # creo las aristas de la gráfica.
        contadorx = 1
        contadory = 1
        peso = 0
        fila = terreno_elegido.datos.matriz.fila
        while fila:
            if fila is not None:
                casilla = fila.casilla
                while casilla:
                    if casilla is not None:
                        if casilla.siguiente is not None:
                            peso = int(casilla.valor) + int(casilla.siguiente.valor)
                        else:
                            break
                        grafica.agregarArista(str(contadorx) + "," + str(contadory), str(str(contadorx) + "," + str(contadory + 1)), peso)
                        contadory += 1
                    else:
                        break
                    casilla = casilla.siguiente
                contadorx += 1
                contadory = 1
            else:
                break
            fila = fila.siguiente

        contadorx = 1
        contadory = 1
        peso = 0
        fila = terreno_elegido.datos.matriz.fila
        casilla2 = fila.siguiente.casilla
        while fila:
            if fila is not None:
                casilla = fila.casilla
                while casilla:
                    if casilla is not None:
                        if fila.siguiente is not None:
                            peso = int(casilla.valor) + int(casilla2.valor)
                        else:
                            break
                        grafica.agregarArista(str(contadorx) + "," + str(contadory), str(contadorx+1) + "," + str(contadory), peso)
                        contadory += 1
                    else:
                        break
                    casilla = casilla.siguiente
                    casilla2 = casilla2.siguiente
                contadorx += 1
                contadory = 1
            else:
                break
            fila = fila.siguiente
            if fila.siguiente is not None:
                casilla2 = fila.siguiente.casilla
            else:
                break

        resultado = grafica.aEstrella(terreno_elegido.datos.xini + "," + terreno_elegido.datos.yini, terreno_elegido.datos.xf + "," + terreno_elegido.datos.yf)
        costo = self.costo(resultado, terreno_elegido)
        matriz_resultado = self.matrizResultado(resultado, terreno_elegido)

        # imprimo el camino
        concatenar = ""
        fila = matriz_resultado.fila
        while fila:
            if fila is not None:
                casilla = fila.casilla
                while casilla:
                    if casilla is not None:
                        concatenar = concatenar + str(casilla.valor) + " "
                    else:
                        break
                    casilla = casilla.siguiente
            else:
                break
            print(concatenar)
            concatenar = ""
            fila = fila.siguiente
            print("\n")
        print("El costo es: " + str(costo))
        a = 1


    def quickSort(self, camino):
        longitud = len(camino)
        if longitud <= 1:
            return camino
        else:
            pivote = camino.pop()
        elementos_mayores = []
        elementos_menores = []
        for elemento in camino:
            if int(elemento.replace(",", "")) > int(pivote.replace(",", "")):
                elementos_mayores.append(elemento)
            else:
                elementos_menores.append(elemento)

        return self.quickSort(elementos_menores) + [pivote] + self.quickSort(elementos_mayores)


    def costo(self, camino, terreno):
        costo = 0
        contador2 = 0
        fila = terreno.datos.matriz.fila
        camino_ordenado = self.quickSort(copy.deepcopy(camino))
        while fila:
            if fila is not None:
                casilla = fila.casilla
                while casilla:
                    if casilla is not None:
                        if contador2<=len(camino_ordenado)-1  and casilla.x == camino_ordenado[contador2].split(",")[0]:
                            if casilla.x + "," + casilla.y == camino_ordenado[contador2]:
                                costo += int(casilla.valor)
                                contador2 += 1
                        else:
                            break
                    else:
                        break
                    casilla = casilla.siguiente
            else:
                break
            fila = fila.siguiente
        return costo

    def matrizResultado(self, camino, terreno):
        contador = 0
        fila = terreno.datos.matriz.fila
        lista_casillas = Fila()
        matriz = Matriz()
        # copio el terreno original
        while fila:
            if fila is not None:
                casilla = fila.casilla
                while casilla:
                    if casilla is not None:
                        lista_casillas.append(casilla.x, casilla.y, casilla.valor)
                    else:
                        break
                    casilla = casilla.siguiente
            else:
                break
            fila = fila.siguiente
            matriz.append(lista_casillas)
            lista_casillas = Fila()

        fila = matriz.fila
        while fila:
            if fila is not None:
                casilla = fila.casilla
                while casilla:
                    if casilla is not None:
                        while contador <= len(camino)-1:
                            if casilla.x+","+casilla.y != camino[contador]:
                                casilla.valor = 0
                            else:
                                casilla.valor = 1
                                break
                            contador += 1
                    else:
                        break
                    casilla = casilla.siguiente
                    contador = 0
            else:
                break
            fila = fila.siguiente
        return matriz

    def mostrarDatos(self):
        print("Pablo Alejandro Franco Lemus")
        print("201708993")
        print("Introducción a la programacion y Computación 2")
        print("Ingenieria en Ciencias y Sistemas")
        print("4to Semestre")

Main().menu()