

class EstacionObj:
    def __init__(self, nombre, estado, color):
        self.nombre = nombre
        self.estado = estado
        self.color = color

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_estado(self):
        return self.estado

    def set_estado(self, estado):
        self.estado = estado
