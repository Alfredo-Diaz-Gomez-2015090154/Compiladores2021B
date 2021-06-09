from copy import copy

class TablaLL1:
    def __init__(self, no_terminales, terminales):
        self.filas = {}
        for no_terminal in no_terminales:
            self.filas[no_terminal] = {}
            for terminal in terminales:
                self.filas[no_terminal][terminal] = []
            self.filas[no_terminal]['$'] = []

    def llenar(self, gic):

        for indice_produccion, produccion in enumerate(gic.producciones):
            
            primero_calculado = gic.primero(produccion[1])
            for p in primero_calculado:
                if p != '':
                    self.agregar_produccion(produccion[0], p, indice_produccion)


            if '' in primero_calculado:
                siguiente_calculado = gic.siguiente(produccion[0])
                for s in siguiente_calculado:
                    self.agregar_produccion(produccion[0], s, indice_produccion)        

    def agregar_produccion(self, no_terminal, terminal, indice_produccion):
        self.filas[no_terminal][terminal].append(indice_produccion)

    def imprimir(self, gic):

        def list_to_str(lst):
            str_final = ''
            for e in lst:
                str_final += str(e) + ','
            return str_final

        print(f'{"" : <7} {gic.terminales[0] : <4}', end='')
        if len(gic.terminales) > 1:
            for terminal in gic.terminales[1:]:
                print(f'    {terminal : <4}', end='')
            print(f'    {"$" : <4}')

        for no_terminal in gic.no_terminales:
            print(f'{no_terminal : <8}', end='')

            producciones_str = list_to_str(self.filas[no_terminal][gic.terminales[0]])
            print(f'{producciones_str : <8}', end='')

            for terminal in gic.terminales[1:]:
                producciones_str = list_to_str(self.filas[no_terminal][terminal])
                print(f'{producciones_str : <8}', end='')                
                
            producciones_str = list_to_str(self.filas[no_terminal]['$'])
            print(f'{producciones_str : <8}', end='')

            print()


    def analisis_LL1(self, cadena, gic):

        cadena_extendida = copy(cadena)
        cadena_extendida.append('$')
        i_cadena = 0
        pila = ['$', gic.inicial]
        
        while pila[-1] != '$':

            if pila[-1] == cadena_extendida[i_cadena]:
                i_cadena += 1
                pila.pop()
            elif pila[-1] in gic.terminales:
                return 0
            else:
                entrada_tablaLL1 = self.filas[pila[-1]][cadena_extendida[i_cadena]]
                if len(entrada_tablaLL1) == 0:
                    return 0
                elif len(entrada_tablaLL1) == 1:
                    pila.pop()
                    if len(gic.producciones[entrada_tablaLL1[0]][1]) == 1:
                        if gic.producciones[entrada_tablaLL1[0]][1][0] != '':
                            pila.append(gic.producciones[entrada_tablaLL1[0]][1][0])
                    else:
                        for e in reversed(gic.producciones[entrada_tablaLL1[0]][1]):
                            pila.append(e)
                elif len(entrada_tablaLL1) > 1:
                    return -1

        return 1

