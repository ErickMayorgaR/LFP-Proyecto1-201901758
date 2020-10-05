from tkinter import Tk
from tkinter import filedialog
from CargarArchivo import ArchivoCarga


def cargar_archivo():
    ruta = filedialog.askopenfilename(filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    Tk().withdraw()
    file = open(ruta, "r", encoding='utf-8')
    print(file)
    info = file.read()

    ir_seleccion = ArchivoCarga()
    ir_seleccion.analisis(info)

def graficar_ruta():
    print("algo")


def graficar_mapa():
    print("algo")


def opciones():
    print("\n")
    print("Proyecto1 LFP Erick Ivan Mayorga Rodriguez 201901758")
    print("Seleccione una Opcion")
    print("1.Cargar Archivo ")
    print("2.Graficar Ruta")
    print("3.Graficar Mapa")
    print("4.Salir")


def main_menu():
    opcion = -1
    while opcion != 4:
        opciones()
        opcion = int(input())
        if opcion == 1:
            cargar_archivo()
        else:
            print("Algo")


main_menu()
"""def separador():
    print("algo") """
