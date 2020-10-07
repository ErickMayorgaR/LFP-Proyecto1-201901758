import re
from RutaObj import *
from EstacionObj import *
import os


class ArchivoCarga:
    nombre_mapa = ""
    errores = [[]]
    tokens = [[]]
    rutas = []
    estaciones = []

    def una_rutaObj(self, nombre, peso, inicio, fin):
        objeto_nuevo = RutaObj(nombre, peso, inicio, fin)
        self.rutas.append(objeto_nuevo)
    def una_estacionObj(self, nombre, estado, color):
        objeto_nuevo = EstacionObj(nombre, estado, color)
        self.estaciones.append(objeto_nuevo)


    def escribeinfo(self,info,file,segundaCol,UltimaCol):
        file.write("No. ; Lexema ; Fila ; Columna ;"+ UltimaCol)
        for x in range(0, len(info)):

            for y in range (0, len (info[x])):
               file.write(str(info[x][y]))
               file.write(";")
            file.write("\n")



    def crearcsv(self,tokens, errores):
        with open ("C:/Users/Erick Mayorga/Desktop/LFP-Proyecto1-201901758/Tokens.csv",'w', encoding= 'utf-8') as file:
            self.escribeinfo(tokens, file,"Lexema", "Token")

        with open("C:/Users/Erick Mayorga/Desktop/LFP-Proyecto1-201901758/Errores.csv", 'w', encoding='utf-8') as file:
            self.escribeinfo(errores, file,"Caracter", "Descripcion")


    def analisis(self, todainformacion):
        informacion = todainformacion.split("\n")

        numero_token = 0
        numero_error = 0
        patron_etiqueta = r"[a-zA-z]"
        patron_numero = r"[0-9]"
        descripcion1 = "Token_apertura"
        descripcion2 = "Token_cierre"
        descripcion3 = "Token_Barra"
        descripcion4 = "Token_ID"
        descripcion_ruta = "Token_ruta"
        descripcion_estacion = "Token_estacion"
        descripcion_estado = "Token_estado"
        descripcion_color = "Token_color"
        descripcion_peso = "Token_peso"


        error1= "Caracter Desconocido"
        error2= "Escritura Etiqueta"
        error3 = "En Etiqueta"

        estado = 0
        fila = 0

        un_token = []
        un_error = []

        estado_error = False

        ruta = False
        estacion = False
        nombre= False
        color = False
        peso = False
        estado_estacion = False
        inicio = False
        fin = False
        lexema = ""

        #una_ruta = RutaObj
        #una_estacion = EstacionObj


        for linea in informacion:

            columna = 0
            fila += 1
            for caracter in linea:
                columna += 1

                if caracter == "\n" or caracter == ' ':
                    continue


                elif estado == 0:
                    if caracter == "<":
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion1]
                        self.tokens.append(un_token)
                        estado = 1
                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila,columna, error1]
                        self.errores.append(un_error)


                elif estado == 1:
                    if re.search(patron_etiqueta, caracter):
                        lexema += caracter

                    elif caracter == "/":
                        estado = 10
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion3]
                        self.tokens.append(un_token)

                    elif caracter == ">":
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion2]
                        self.tokens.append(un_token)

                        numero_token += 1
                        un_token = [numero_token, lexema, fila, (columna - len(lexema)), descripcion4]
                        self.tokens.append(un_token)


                        if lexema.lower() == "ruta":
                            ruta = True
                            una_ruta = RutaObj("","","","")
                        elif lexema.lower() == "estacion":
                            estacion = True
                            una_estacion = None

                            una_estacion = EstacionObj("","","")
                        elif lexema.lower() == "nombre":
                            nombre = True
                        elif lexema.lower() == "peso" and ruta == True:
                            peso = True
                        elif lexema.lower() == "color":
                            color = True
                        elif lexema.lower() == "estado":
                            estado_estacion = True
                        elif lexema.lower() == "inicio":
                            estacion = True
                            nombre = True
                            inicio = True
                        elif lexema.lower() == "fin":
                            estacion = True
                            nombre = True
                            fin = True

                        estado = 2

                        lexema = ""

                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila,columna, error2]
                        self.errores.append(un_error)

                elif estado == 2:
                    if caracter == "<":
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion1]
                        self.tokens.append(un_token)
                        estado = 1
                    elif ruta == True and nombre == True:
                        if (re.search(patron_etiqueta, caracter)) or (caracter == "_") or (re.search(patron_numero, caracter)):
                            estado = 3
                            lexema += caracter
                        else:
                            numero_error += 1
                            un_error = [numero_error, caracter, fila, columna, error2]
                            self.errores.append(un_error)
                    elif ruta == False and estacion == False and nombre == True:
                        if (re.search(patron_etiqueta, caracter)) or (caracter == "_") or (
                                re.search(patron_numero, caracter)):
                            estado = 3
                            lexema += caracter
                        else:
                            numero_error += 1
                            un_error = [numero_error, caracter, fila, columna, error2]
                            self.errores.append(un_error)
                    elif estacion == True and nombre == True:
                        if re.search(patron_etiqueta, caracter) or re.search(patron_numero, caracter):
                            estado = 4
                            lexema += caracter
                        else:
                            numero_error += 1
                            un_error = [numero_error, caracter, fila, columna, error1]
                            self.errores.append(un_error)
                    elif color == True:
                        if caracter == "#":
                            estado = 5
                            lexema += caracter
                        else:
                            numero_error += 1
                            un_error = [numero_error, caracter, fila, columna, error1]
                            self.errores.append(un_error)
                    elif peso == True:
                        if re.search(patron_numero, caracter):
                            estado = 6
                            lexema += caracter
                        else:
                            numero_error += 1
                            un_error = [numero_error, caracter, fila, columna, error1]
                            self.errores.append(un_error)
                    elif estado_estacion == True:
                        if re.search(patron_etiqueta, caracter):
                            lexema += caracter
                            estado = 8
                        else:
                            numero_error += 1
                            un_error = [numero_error, caracter, fila, columna, error1]
                            self.errores.append(un_error)
                elif estado == 3:
                    if (re.search(patron_etiqueta, caracter)) or (caracter == "_") or (
                    re.search(patron_numero, caracter)):
                        lexema += caracter
                    elif caracter == "<":
                        if ruta == False and estacion == False:
                            estado = 9
                            numero_token += 1
                            un_token = [numero_token, caracter, fila, columna, descripcion2]
                            self.tokens.append(un_token)

                            numero_token += 1
                            un_token = [numero_token, lexema, fila, (columna - len(lexema)), descripcion_ruta]
                            self.tokens.append(un_token)

                            self.nombre_mapa = lexema

                            lexema = ""

                        else:
                            estado = 9
                            numero_token += 1
                            un_token = [numero_token, caracter, fila, columna, descripcion2]
                            self.tokens.append(un_token)

                            numero_token += 1
                            un_token = [numero_token, lexema, fila, (columna - len(lexema)), descripcion_ruta]
                            self.tokens.append(un_token)

                            if inicio == True:
                                una_ruta.set_inicio(lexema)
                            elif fin == True:
                                una_ruta.set_fin(lexema)
                            else:
                                una_ruta.set_nombre(lexema)
                            #print(lexema)
                            #print(ruta)
                            #print(estacion)

                            lexema = ""

                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila, columna, error1]
                        self.errores.append(un_error)
                elif estado == 4:
                    if re.search(patron_etiqueta, caracter) or re.search(patron_numero, caracter):
                        lexema += caracter
                    elif caracter == "<":
                        estado = 9
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion2]
                        self.tokens.append(un_token)

                        numero_token += 1
                        un_token = [numero_token, lexema, fila, (columna - len(lexema)), descripcion_estacion]
                        self.tokens.append(un_token)

                        if inicio == True:
                            una_ruta.set_inicio(lexema)
                        elif fin == True:
                            una_ruta.set_fin(lexema)
                        else:
                            una_estacion.set_nombre(lexema)



                        lexema = ""
                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila, columna, error1]
                        self.errores.append(un_error)
                elif estado == 5:
                    if re.search(patron_etiqueta, caracter) or re.search(patron_numero, caracter):
                        lexema += caracter
                    elif caracter == "<":
                        estado = 9
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion2]
                        self.tokens.append(un_token)

                        numero_token += 1
                        un_token = [numero_token, lexema, fila, (columna - len(lexema)), descripcion_color]
                        self.tokens.append(un_token)

                        una_estacion.set_color(lexema)



                        lexema = ""
                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila, columna, error1]
                        self.errores.append(un_error)
                elif estado == 6:
                    if re.search(patron_numero, caracter):
                        lexema += caracter
                    elif caracter == ".":
                        estado = 7
                        lexema += caracter
                    elif caracter == "<":


                        estado = 9
                        numero_token += 1
                        un_token = [numero_token, lexema, fila, (columna - len(lexema)), descripcion_peso]
                        self.tokens.append(un_token)


                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion2]
                        self.tokens.append(un_token)
                        una_ruta.set_peso(lexema)

                        lexema = ""
                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila, columna, error1]
                        self.errores.append(un_error)
                elif estado == 7:
                    if re.search(patron_numero, caracter):
                        lexema += caracter

                    elif caracter == "<":
                        estado = 9
                        numero_token += 1
                        un_token = [numero_token, lexema, fila, (columna - len(lexema)), descripcion_peso]
                        self.tokens.append(un_token)

                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion2]
                        self.tokens.append(un_token)


                        una_ruta.set_peso(lexema)

                        lexema = ""


                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila, columna, error1]
                        self.errores.append(un_error)

                elif estado == 8:
                    if re.search(patron_etiqueta, caracter):
                        lexema += caracter
                    elif caracter == "<":
                        estado = 9
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion2]
                        self.tokens.append(un_token)

                        numero_token += 1
                        un_token = [numero_token, lexema, fila, (columna - len(lexema)), descripcion_estado]
                        self.tokens.append(un_token)

                        if lexema.lower() == "disponible":
                            una_estacion.set_estado(True)
                        elif lexema.lower() == "cerrado":
                            una_estacion.set_estado(False)

                        lexema = ""
                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila, columna, error1]
                        self.errores.append(un_error)

                elif estado == 9:
                    if caracter == "/":
                        estado = 10
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion3]
                        self.tokens.append(un_token)
                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila, columna, error1]
                        self.errores.append(un_error)
                elif estado == 10:
                    if re.search(patron_etiqueta, caracter):
                        lexema += caracter
                    elif caracter == ">":
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion2]
                        self.tokens.append(un_token)

                        numero_token += 1
                        un_token = [numero_token, lexema, fila , columna - len(lexema), descripcion4]
                        self.tokens.append(un_token)


                        if lexema.lower() == "ruta":
                            ruta = False
                            self.una_rutaObj(una_ruta.get_nombre(), una_ruta.get_peso(), una_ruta.get_inicio(), una_ruta.get_fin())
                            una_ruta = RutaObj("","","","")
                        elif lexema.lower() == "estacion":
                            estacion = False
                            self.una_estacionObj(una_estacion.get_nombre(), una_estacion.get_estado(), una_estacion.get_color())



                            una_estacion = EstacionObj("","","")
                        elif lexema.lower() == "nombre":
                            nombre = False
                        elif lexema.lower() == "peso":
                            peso = False
                        elif lexema.lower() == "color":
                            color = False
                        elif lexema.lower() == "estado":
                            estado_estacion = False
                        elif lexema.lower() == "inicio":
                            estacion = False
                            nombre = False
                            inicio = False
                        elif lexema.lower() == "fin":
                            estacion = False
                            nombre = False
                            fin = False
                        estado = 11
                        lexema = ""

                elif estado == 11:
                    if caracter == "<":
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion1]
                        self.tokens.append(un_token)
                        estado = 1
                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila,columna, error1]
                        self.errores.append(un_error)

        #print(self.tokens)
        self.rutas= self.rutas
        self.crearcsv(self.tokens, self.errores)
        print(self.rutas[1].get_nombre())
        print(self.rutas[1].get_peso(), "?")
        print(self.rutas[1].get_inicio())
        print(self.rutas[1].get_fin())
        print(self.nombre_mapa + "??? xd")
        print(self.estaciones[0].get_nombre())
        print(self.estaciones[1].get_nombre())
        print(self.estaciones[2].get_nombre())









