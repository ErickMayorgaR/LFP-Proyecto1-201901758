import os

class CargarMapa:
    nodos_estaciones = []
    nodos_rutas = []

    #def calcularMejorRuta(self):
    def ordenar(self, nombreMapa, rutas, estaciones):

        for estacion in estaciones:
            nodo = ""
            p2 = ' style=filled fillcolor= "'
            p1 = '[label = "'
            if estacion.get_estado() == True:
                nodo = estacion.get_nombre() + p1 + estacion.get_nombre() + '\ndisponible" ' + p2 + estacion.get_color() +'"' +"]"
                print(nodo)
                self.nodos_estaciones.append(nodo)
            else:
                nodo = estacion.get_nombre() + p1 + estacion.get_nombre() + '\ncerrada "' + p2 + estacion.get_color() +'"'+ "]"
                print(nodo)
                self.nodos_estaciones.append(nodo)

        for ruta in rutas:
            p1 = '[label ="'
            nodo = ruta.get_inicio().upper() + "->" + ruta.get_fin().upper() + p1 + ruta.get_nombre() + "\n" + ruta.get_peso()+ ' "]'
            self.nodos_rutas.append(nodo)

        self.graficar(nombreMapa)


    def graficar(self, nombreMapa):
        file = open("Prueba.dot", "w")

        file.write("digraph D {" + "\n")
        file.write("rankdir= LR" + "\n")
        for nodo in self.nodos_estaciones:

            print(nodo + "Este es el nodo")
            file.write(nodo+ "\n")
        for nodo in self. nodos_rutas:
            file.write(nodo + "\n")

        file.write('label = "' + nombreMapa+ '" ;')
        file.write("}")
        file.close()
        os.system('dot -Tpng Prueba.dot -o P1.png')
        os.system("P1.png")


