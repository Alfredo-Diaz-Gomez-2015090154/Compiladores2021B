import copy

class Estado:

    def __init__(self, nombre, kernel, estados_AFND):
        self.nombre = nombre
        self.kernel = copy.copy(kernel)
        self.estados_AFND = copy.copy(estados_AFND)