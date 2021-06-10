import copy

class AFD:

    def __init__(self, alfabeto):
        self.alfabeto = copy.copy(alfabeto)
        self.transiciones = {}

    def copiar_estados(self, estados_generados):
        self.estados = estados_generados.copy()

    def copiar_estado_inicial(self, estado_inicial):
        self.estado_inicial = estado_inicial

    def copiar_estados_finales(self, estados_finales):
        self.estados_finales = estados_finales

    def agregar_estado(self, estado_actual, entrada, estado_siguiente):
        self.transiciones[(estado_actual, entrada)] = estado_siguiente
    
    def determinar_estado_pozo(self, estado_pozo):
        self.estado_pozo = estado_pozo

    def mostrar_elementos(self):
        print(f'Alfabeto: {self.alfabeto}')
        print(f'Estados: {self.estados}')
        print(f'Estado inicial: {self.estado_inicial}')
        print(f'Estados finales: {self.estados_finales}')
        print("Transiciones (Sin estado pozo): ")
        for llave in self.transiciones.keys():
            if not self.transiciones[llave] == self.estado_pozo:
                print(f"{llave} -> {self.transiciones[llave]}")
        mostrar_pozo = input("¿Mostrar pozo? (1 = Sí): ")
        if mostrar_pozo == '1':
            for llave in self.transiciones.keys():
                if self.transiciones[llave] == self.estado_pozo:
                    print(f"{llave} -> {self.transiciones[llave]}")            
        