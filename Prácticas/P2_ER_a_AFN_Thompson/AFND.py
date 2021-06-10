from os import system, mkdir
from os.path import isdir
import copy, json

class AFND:

    def __init__(self, estados, inicial, finales, transiciones):
        self.estados = copy.copy(estados)
        self.estado_inicial = inicial
        self.finales = copy.copy(finales)
        self.transiciones = copy.deepcopy(transiciones)

    def numerar_estados(self):

        estado_numero = {}
        contador_estados = {"valor" : len(self.estados)}

        estados_visitados = []
        llaves_transiciones = {}

        for llave in self.transiciones.keys():
            if llave[0] not in llaves_transiciones.keys():
                llaves_transiciones[llave[0]] = [llave]
            else:
                llaves_transiciones[llave[0]].append(llave)
        

        def dfs_post(self, estado):
            estados_visitados.append(estado)
            if estado in llaves_transiciones.keys():
                for relacion_transicion in llaves_transiciones[estado]:
                    for siguiente_estado in reversed(self.transiciones[relacion_transicion]):
                        if siguiente_estado not in estados_visitados:
                            dfs_post(self, siguiente_estado)
            estado_numero[estado] = contador_estados["valor"]
            contador_estados["valor"] -= 1
        
        dfs_post(self, self.estado_inicial)

        #print(estado_numero)

        self.estado_inicial = estado_numero[self.estado_inicial]
        nuevos_finales = []
        for final in self.finales:
            nuevos_finales.append(estado_numero[final])
        self.finales = nuevos_finales

        nuevas_transiciones = {}
        for relacion_transicion in self.transiciones:
            aux_relacion_transicion = (estado_numero[relacion_transicion[0]], relacion_transicion[1])
            nuevas_transiciones[aux_relacion_transicion] = []
            for siguiente_estado in self.transiciones[relacion_transicion]:
                nuevas_transiciones[aux_relacion_transicion].append(estado_numero[siguiente_estado])

        self.transiciones = nuevas_transiciones
        self.estados = [i for i in range(1, len(self.estados)+1)]


    @staticmethod
    def unitaria(c, contador_c):

        # Definiendo el conjunto de estados.
        estado_0 = f'{c}_{contador_c}_1'
        estado_1 = f'{c}_{contador_c}_2'
        estados = [estado_0, estado_1]

        # Definiendo el estado inicial y los estados finales.
        estado_inicial = estado_0
        estados_finales = [estado_1]

        # Definiendo las transiciones.
        transiciones = {}
        transiciones[(estado_0, c)] = [estado_1]

        return AFND(estados, estado_inicial, estados_finales, transiciones)
    
    @staticmethod
    def epsilon(contador_E):
        # Definiendo el conjunto de estados.
        estado_0 = f'E_{contador_E}_1'
        estado_1 = f'E_{contador_E}_2'
        estados = [estado_0, estado_1]

        # Definiendo el estado inicial y los estados finales.
        estado_inicial = estado_0
        estados_finales = [estado_1]

        # Definiendo las transiciones.
        transiciones = {}
        transiciones[(estado_0, 'E')] = [estado_1]

        return AFND(estados, estado_inicial, estados_finales, transiciones)        

    @staticmethod
    def estrella(afnd_entrada, contador_operacion):

        # Definiendo los estados.
        estado_0 = f'R_{contador_operacion}_1'
        estado_1 = f'R_{contador_operacion}_2'
        estados = [estado_0, estado_1]
        estados.extend(afnd_entrada.estados)

        # Definiendo el estado inicial y los estados finales.
        estado_inicial = estado_0
        estados_finales = [estado_1]

        # Definiendo las transiciones.
        transiciones = copy.deepcopy(afnd_entrada.transiciones)
        transiciones[(estado_0, 'E')] = [afnd_entrada.estado_inicial, estado_1]
        transiciones[(afnd_entrada.finales[0], 'E')] = [afnd_entrada.estado_inicial, estado_1]

        return AFND(estados, estado_inicial, estados_finales, transiciones)
    
    @staticmethod
    def concatenacion(afnd_1, afnd_2, contador_operacion):

        # Definiendo los estados.
        estados = copy.copy(afnd_1.estados)
        estados.extend(afnd_2.estados)
        estados.remove(afnd_2.estado_inicial)

        # Definiendo el estado inicial y los estados finales.
        estado_inicial = afnd_1.estado_inicial
        estados_finales = afnd_2.finales

        # Definiendo las transiciones.
        transiciones = copy.deepcopy(afnd_1.transiciones)
        transiciones.update(afnd_2.transiciones)
        for key in afnd_2.transiciones.keys():
            if afnd_2.estado_inicial in key:
                transiciones[(afnd_1.finales[0], key[1])] = copy.copy(afnd_2.transiciones[key])
                transiciones.pop(key, None)

        return AFND(estados, estado_inicial, estados_finales, transiciones)

    @staticmethod
    def union(afnd_1, afnd_2, contador_operacion):

        # Definiendo los estados.
        estado_0 = f'R_{contador_operacion}_1'
        estado_1 = f'R_{contador_operacion}_2'
        estados = [estado_0, estado_1]
        estados.extend(afnd_1.estados)
        estados.extend(afnd_2.estados)

        # Definiendo el estado inicial y los estados finales.
        estado_inicial = estado_0
        estados_finales = [estado_1]

        # Definiendo las transiciones.
        transiciones = copy.deepcopy(afnd_1.transiciones)
        transiciones.update(afnd_2.transiciones)
        transiciones[(estado_0, 'E')] = [afnd_1.estado_inicial, afnd_2.estado_inicial]
        transiciones[(afnd_1.finales[0], 'E')] = [estado_1]
        transiciones[(afnd_2.finales[0], 'E')] = [estado_1]

        return AFND(estados, estado_inicial, estados_finales, transiciones)        

    def afnd_json(self):

        dictionary_aux = {"alfabeto" : self.alfabeto,
                          "estados" : self.estados, 
                          "estado_inicial" : self.estado_inicial,
                          "estados_finales" : self.finales,
                          "transiciones" : {}
                        }

        for transicion in self.transiciones.keys():
            dictionary_aux["transiciones"][f"({transicion[0]}, {transicion[1]})"] = self.transiciones[transicion]

        if not isdir('resultados'):
            mkdir('resultados')


        with open("resultados/resultado.json", "w") as outfile:
            json.dump(dictionary_aux, outfile)

    def mostrar_informacion(self):
        print(f"Alfabeto: {self.alfabeto}")
        print(f"Estados: {self.estados}")
        print(f"Estado inicial: {self.estado_inicial}")
        print(f"Estados finales: {self.finales}")
        print(f"Transiciones: ")
        for key in self.transiciones.keys():
            print(f"{key} : {self.transiciones[key]}")

