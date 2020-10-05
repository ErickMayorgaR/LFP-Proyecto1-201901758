import re


class ArchivoCarga:
    errores = [[]]
    tokens = [[]]

    def analisis(self, informacion):
        numero_token = 0
        numero_error = 0
        patron_etiqueta = r"[a-zA-z]"
        patron_numero = r"[0-9]"
        descripcion1 = "Token_apertura"
        descripcion2 = "Token_cierre"
        descripcion3 = "Token_Barra"
        descripcion4 = "Token_ID"
        descripcion_ruta= "Token_ruta"
        descripcion_estacion= "Token_estacion"
        descripcion_estado = "Token_estado"
        descripcion_nombre = "Token_ruta"
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
        lexema = ""


        for linea in informacion:
            columna = 0
            fila += 1
            for caracter in linea:
                columna += 1


                if caracter == "\n" or caracter == "":
                    continue

                if estado == 0:
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

                    elif caracter == ">":
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion2]
                        self.tokens.append(un_token)

                        numero_token += 1
                        un_token = [numero_token, lexema, fila, (columna - len(lexema)), descripcion4]
                        self.tokens.append(un_token)

                        if lexema.lower() == "ruta":
                            ruta = True
                        elif lexema.lower() == "estacion":
                            estacion = True
                        elif lexema.lower() == "nombre":
                            nombre = True
                        elif lexema.lower() == "peso":
                            peso = True
                        elif lexema.lower() == "color":
                            color = True
                        elif lexema.lower() == "estado":
                            estado_estacion = True
                        elif lexema.lower() == "inicio":
                            estado = True
                            nombre = True
                        elif lexema.lower() == "fin":
                            estado = True
                            nombre = True

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
                    elif estacion == True and nombre == True:
                        if re.search(patron_etiqueta, caracter):
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
                        estado = 9
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion2]
                        self.tokens.append(un_token)

                        numero_token += 1
                        un_token = [numero_token, lexema, fila, (columna - len(lexema)), descripcion_ruta]
                        self.tokens.append(un_token)

                        lexema = ""
                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila, columna, error1]
                        self.errores.append(un_error)
                elif estado == 4:
                    if re.search(patron_etiqueta, caracter):
                        lexema += caracter
                    elif caracter == "<":
                        estado = 9
                        numero_token += 1
                        un_token = [numero_token, caracter, fila, columna, descripcion2]
                        self.tokens.append(un_token)

                        numero_token += 1
                        un_token = [numero_token, lexema, fila, (columna - len(lexema)), descripcion_estacion]
                        self.tokens.append(un_token)

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
                        un_token = [numero_token, caracter, fila, columna, descripcion2]
                        self.tokens.append(un_token)

                        numero_token += 1
                        un_token = [numero_token, lexema, fila, (columna - len(lexema)), descripcion_peso]
                        self.tokens.append(un_token)

                        lexema = ""

                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila, columna, error1]
                        self.errores.append(un_error)

                if estado == 8:
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

                        lexema = ""
                    else:
                        numero_error += 1
                        un_error = [numero_error, caracter, fila, columna, error1]
                        self.errores.append(un_error)

                if estado == 9:








