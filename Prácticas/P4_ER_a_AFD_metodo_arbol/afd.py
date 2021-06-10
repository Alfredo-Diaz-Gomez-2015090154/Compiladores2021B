from copy import copy

class Estado:

    def __init__(self, lista_simbolos, nombre):
        
        self.lista_simbolos = copy(lista_simbolos)
        self.nombre = nombre

class AFD:

    def __init__(self, estado_inicial, alfabeto):
        
        self.estado_inicial = estado_inicial
        self.alfabeto = copy(alfabeto)
        self.estados = []
        self.estados.append(Estado([], '0')) # Estado de pozo.
        self.estados.append(self.estado_inicial)
        
        self.transiciones = {}
        self.estados_finales = []

    def agregar_transicion(self, estado_entrada, entrada, estado_siguiente):
        self.transiciones[(estado_entrada, entrada)] = estado_siguiente

    def agregar_estado_final(self, estado_final):
        self.estados_finales.append(estado_final)
        

    def construir_estados(self, tabla_siguientes, simbolos_orden):

        indice_simbolo_final = len(tabla_siguientes)
        estados_revisados = 0
        # print("Inicial: ",self.estados[estados_revisados].lista_simbolos)

        info_estados_siguientes = {}
        for s in self.alfabeto:
            info_estados_siguientes[s] = {}
            info_estados_siguientes[s]['revisado'] = False
            info_estados_siguientes[s]['simbolos'] = []
            info_estados_siguientes[s]['nombre'] = ''

        while estados_revisados < len(self.estados):

            # print(f'Numero estados: {len(self.estados)}, Revisando: {estados_revisados} {self.estados[estados_revisados].nombre}')

            if indice_simbolo_final in self.estados[estados_revisados].lista_simbolos:
                self.agregar_estado_final(self.estados[estados_revisados].nombre)

            for indice_simbolo in self.estados[estados_revisados].lista_simbolos:
                # print(simbolos_orden[indice_simbolo-1])

                if simbolos_orden[indice_simbolo-1] == '#':
                    break

                info_estados_siguientes[simbolos_orden[indice_simbolo-1]]['revisado'] = True

                for siguiente_pos in tabla_siguientes[indice_simbolo]:
                    if siguiente_pos not in info_estados_siguientes[simbolos_orden[indice_simbolo-1]]['simbolos']:
                        info_estados_siguientes[simbolos_orden[indice_simbolo-1]]['simbolos'].append(siguiente_pos)
            
            for simbolo in info_estados_siguientes.keys():
                
                if info_estados_siguientes[simbolo]['revisado']:
                    info_estados_siguientes[simbolo]['simbolos'].sort()
                    for indice_simbolo in info_estados_siguientes[simbolo]['simbolos'][:-1]:
                        info_estados_siguientes[simbolo]['nombre'] += f'{indice_simbolo}_'
                    info_estados_siguientes[simbolo]['nombre'] += f'{info_estados_siguientes[simbolo]["simbolos"][-1]}'

            # for simbolo in info_estados_siguientes.keys():
                # print(info_estados_siguientes[simbolo])

            for simbolo in info_estados_siguientes.keys():
                
                if not info_estados_siguientes[simbolo]['revisado']:
                    info_estados_siguientes[simbolo]['nombre'] = '0'

                is_estado_existente = False

                for estado in self.estados:
                    # print(f'{info_estados_siguientes[simbolo]["nombre"]} || {estado.nombre}')
                    if info_estados_siguientes[simbolo]['nombre'] == estado.nombre:
                        is_estado_existente = True
                        # print("Igual :D")
                        break
                
                if not is_estado_existente:
                    self.estados.append(Estado(info_estados_siguientes[simbolo]['simbolos'], info_estados_siguientes[simbolo]['nombre']))

                self.agregar_transicion(self.estados[estados_revisados].nombre, simbolo, info_estados_siguientes[simbolo]['nombre'])

                # print(info_estados_siguientes[simbolo])
            
            for s in self.alfabeto:
                info_estados_siguientes[s] = {}
                info_estados_siguientes[s]['revisado'] = False
                info_estados_siguientes[s]['simbolos'] = []
                info_estados_siguientes[s]['nombre'] = ''            

            estados_revisados += 1

        # print(f"Estados: {len(self.estados)}")
        #3for estado in self.estados:
            # print(estado.nombre)
