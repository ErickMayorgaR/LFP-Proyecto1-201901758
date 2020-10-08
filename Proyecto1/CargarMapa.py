import os

class CargarMapa:

    inicio = ""
    final = ""
    sumas = []
    todasrutas = []
    peso = 0
    nodos_estaciones = []
    nodos_rutas = []
    mejor_ruta = []


    def graphDemas(self, ruta1, rutas):
        for ruta in rutas:
             if ruta1.get_fin().lower() == ruta.get_inicio().lower() and ruta.get_fin().lower() != ruta1.get_inicio().lower() and ruta.get_inicio().lower() != self.final:
                 self.mejor_ruta.append(ruta)
                 p1 = '[label ="'
                 p2 = 'style = bold '
                 nodo = ruta.get_inicio().lower() + "->" + ruta.get_fin().lower() + p1 + ruta.get_nombre() + "\n" + ruta.get_peso() + '" ' + p2 + ' ]'
                 self.nodos_rutas.append(nodo)
                 ruta2 = ruta.get_fin().lower()
                 for ruta in rutas:
                    if ruta2 == ruta.get_inicio().lower() and ruta.get_fin().lower() != ruta2 and ruta.get_inicio().lower() != self.final:
                        p1 = '[label ="'
                        p2 = 'style = bold '
                        nodo = ruta.get_inicio().lower() + "->" + ruta.get_fin().lower() + p1 + ruta.get_nombre() + "\n" + ruta.get_peso() + '" ' + p2 + ']'
                        self.nodos_rutas.append(nodo)
                        ruta3 = ruta.get_fin().lower()
                        for ruta in rutas:
                            if ruta3 == ruta.get_inicio().lower() and ruta.get_inicio().lower() != self.inicio.lower():
                                p1 = '[label ="'
                                p2 = 'style = bold '
                                nodo = ruta.get_inicio().lower() + "->" + ruta.get_fin().lower() + p1 + ruta.get_nombre() + "\n" + ruta.get_peso() + '" ' + p2 + ']'
                                self.nodos_rutas.append(nodo)
                                ruta4 = ruta.get_inicio().lower()

        return

    def graficarMejorRuta(self,nombreMapa,mejorInicio, rutas, estaciones):
        for ruta in rutas:
            if mejorInicio == ruta:
                self.mejor_ruta.append(mejorInicio)
                p1 = '[label ="'
                p2 = 'style = bold '
                nodo = ruta.get_inicio().lower() + "->" + ruta.get_fin().lower() + p1 + ruta.get_nombre() + "\n" + ruta.get_peso() + '" ' + p2 + ']'
                self.nodos_rutas.append(nodo)
                self.graphDemas(mejorInicio, rutas)
                continue

        for estacion in estaciones:
            for ruta in self.mejor_ruta:
                if ruta.get_inicio().lower() == estacion.get_nombre().lower():
                    nodo = ""
                    p2 = ' style=filled fillcolor= "'
                    p1 = '[label = "'
                    if estacion.get_estado() == True:
                        nodo = estacion.get_nombre().lower() + p1 + estacion.get_nombre() + '\ndisponible" ' + p2 + estacion.get_color() + '"' + "]"
                    self.nodos_estaciones.append(nodo)
                elif self.final == estacion.get_nombre().lower():
                    nodo = ""
                    p2 = ' style=filled fillcolor= "'
                    p1 = '[label = "'
                    if estacion.get_estado() == True:
                        nodo = estacion.get_nombre().lower() + p1 + estacion.get_nombre() + '\ndisponible" ' + p2 + estacion.get_color() + '"' + "]"
                    self.nodos_estaciones.append(nodo)
        self.graficar(nombreMapa)



    def sumasRutas(self, ruta1, rutas):
        for ruta in rutas:
            if ruta1.get_fin().lower() == ruta.get_inicio().lower() and ruta.get_fin().lower() != ruta1.get_inicio().lower() and ruta.get_inicio().lower() != self.final:
                self.peso += float(ruta.get_peso())
                ruta2 = ruta.get_fin().lower()

                for ruta in rutas:
                    if ruta2 == ruta.get_inicio().lower() and ruta.get_fin().lower() != ruta2 and ruta.get_inicio().lower() != self.final:
                        self.peso += float(ruta.get_peso())
                        ruta3 = ruta.get_fin().lower()

                        for ruta in rutas:
                            if ruta3 == ruta.get_inicio().lower() and ruta.get_fin().lower() != ruta3 and ruta.get_inicio().lower() != self.final:
                                self.peso += float(ruta.get_peso())

        self.sumas.append(self.peso)
        self.peso = 0

        return


    def calcularMejorRuta(self, nombreMapa, rutas, estaciones):
        print("Por favor ingrese una ruta de inicio")
        self.inicio = input()
        print("Por favor ingrese una ruta final")
        self.final = input()

        size = len(rutas)

        for ruta in rutas:
            if ruta.get_inicio().lower() == self.inicio.lower():
                self.todasrutas.append(ruta)
                self.peso += float(ruta.get_peso())
                self.sumasRutas(ruta, rutas)


        posicion = self.sumas.index(min(self.sumas))
        print(self.sumas)
        print(posicion)
        print(self.todasrutas[0].get_nombre())
        print(self.todasrutas[1].get_nombre())
        mejorinicio = self.todasrutas[posicion]
        self.graficarMejorRuta(nombreMapa, mejorinicio, rutas, estaciones)




    def ordenar(self, nombreMapa, rutas, estaciones):


        for estacion in estaciones:
            nodo = ""
            p2 = ' style=filled fillcolor= "'
            p1 = '[label = "'
            if estacion.get_estado() == True:
                nodo = estacion.get_nombre().lower() + p1 + estacion.get_nombre() + '\ndisponible" ' + p2 + estacion.get_color() +'"' +"]"

                self.nodos_estaciones.append(nodo)
            else:
                nodo = estacion.get_nombre().lower() + p1 + estacion.get_nombre() + '\ncerrada "' + p2 + estacion.get_color() +'"'+ "]"

                self.nodos_estaciones.append(nodo)

        for ruta in rutas:
            p1 = '[label ="'
            p2 = 'style = bold '

            nodo = ruta.get_inicio().lower() + "->" + ruta.get_fin().lower() + p1 + ruta.get_nombre() + "\n" + ruta.get_peso()+ ' "]'
            self.nodos_rutas.append(nodo)

        self.graficar(nombreMapa)


    def graficar(self, nombreMapa):
        file = open("Prueba.dot", "w")

        file.write("digraph D {" + "\n")
        file.write("rankdir= LR" + "\n")
        for nodo in self.nodos_estaciones:


            file.write(nodo+ "\n")
        for nodo in self. nodos_rutas:
            file.write(nodo + "\n")

        file.write('label = "' + nombreMapa+ '" ;' + "\n")
        file.write("}")
        file.close()
        os.system('dot -Tpng Prueba.dot -o P1.png')
        os.system("P1.png")


