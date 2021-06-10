class Nodo:

    def __init__(self):
        self.is_anulable = None
    
class NoEpsilon(Nodo):
    
    def __init__(self):
        super().__init__()
        self.primera = None
        self.ultima = None

class Hoja(NoEpsilon):

    def __init__(self, posicion, simbolo):
        super().__init__()
        self.posicion = posicion
        self.simbolo = simbolo
        self.is_anulable = False
        self.primera = [posicion]
        self.ultima = [posicion]

class Interno(NoEpsilon):

    def __init__(self, operacion, hijo_izquierdo, hijo_derecho = None):
        super().__init__()
        self.operacion = operacion
        self.hijo_izquierdo = hijo_izquierdo
        self.hijo_derecho = hijo_derecho

    def postorden_tabla_siguiente(self, tabla_siguientes):

        if self.hijo_izquierdo is not None and not isinstance(self.hijo_izquierdo, Hoja):
            self.hijo_izquierdo.postorden_tabla_siguiente(tabla_siguientes)

        if self.hijo_derecho is not None and not isinstance(self.hijo_derecho, Hoja):
            self.hijo_derecho.postorden_tabla_siguiente(tabla_siguientes)

        # print(self.operacion)

        if self.operacion == '.':
            for ultima_pos_izq in self.hijo_izquierdo.ultima:
                for primera_pos_der in self.hijo_derecho.primera:
                    if primera_pos_der not in tabla_siguientes[ultima_pos_izq]:
                        tabla_siguientes[ultima_pos_izq].append(primera_pos_der)
        elif self.operacion == '*':
            for ultima_pos_asterisco in self.ultima:
                for primera_pos_asterisco in self.primera:
                    if primera_pos_asterisco not in tabla_siguientes[ultima_pos_asterisco]:
                        tabla_siguientes[ultima_pos_asterisco].append(primera_pos_asterisco)
