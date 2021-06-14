from copy import copy

class SubconjuntoLR0:

    def __init__(self, kernel, elementos_LR0, numero):
        self.kernel = copy(kernel)
        self.elementos_LR0 = copy(elementos_LR0)
        self.numero = numero

class ElementoLR0:
    def __init__(self, no_terminal, p_cadena, p_lista, punto_pos, num_produccion):
        self.no_terminal = no_terminal
        self.p_cadena = p_cadena
        self.p_lista = copy(p_lista)
        self.punto_pos = punto_pos
        self.num_produccion = num_produccion

def lista_a_str(lista):
    str_o = ''
    for e in lista:
        str_o += e + ' '

    return str_o

def lista_num_a_str(lista):
    str_o = ''
    for e in lista:
        str_o += str(e) + ' '

    return str_o

def cerradura(subconjunto, gic):

    subconjunto_c = copy(subconjunto)
    subconjunto_lst = list(copy(subconjunto_c))

    no_terminales_pro_agregadas = dict()

    for no_terminal in gic.no_terminales:
        no_terminales_pro_agregadas[no_terminal] = False

    i_elemento = 0
    while i_elemento < len(subconjunto_lst):
        ele_lr0 = subconjunto_lst[i_elemento]
        if ele_lr0.punto_pos != len(ele_lr0.p_lista) - 1:            

            sig_elemento = ele_lr0.p_lista[ele_lr0.punto_pos + 1]
            #print(f"No está al final -> {sig_elemento}")

            if sig_elemento in gic.no_terminales:
                #print("Esta en los no terminales.")
                if not no_terminales_pro_agregadas[sig_elemento]:
                    no_terminales_pro_agregadas[sig_elemento] =  True
                    for i, produccion in enumerate(gic.producciones):
                        
                        if produccion[0] == sig_elemento:

                            # Verificar si produce Épsilon.
                            if len(produccion[1]) == 1 and produccion[1][0] == '':
                                produccion_lst = ['.']
                                cadena_produccion = '.'
                            else:                        
                                produccion_lst = copy(produccion[1])
                                produccion_lst.insert(0, '.')
                                cadena_produccion = lista_a_str(produccion_lst)

                            nuevo_lr0 = ElementoLR0(sig_elemento, cadena_produccion, produccion_lst, 0, i)
                            subconjunto_c.add(nuevo_lr0)
                            subconjunto_lst.append(nuevo_lr0)
        i_elemento += 1

    #for lr0 in subconjunto_lst:
    #    print(f"{lr0.no_terminal} -> {lr0.p_cadena}")        
    
    return subconjunto_c


def mover(subconjunto, X):
    """
    subconjunto : Subconjunto a mover.
    X : Símbolo gramatical.
    """

    subconjunto_mover = set()

    for ele_lr0 in subconjunto:
        if ele_lr0.punto_pos != len(ele_lr0.p_lista) - 1:
            #print("No está en el final.")
            if ele_lr0.p_lista[ele_lr0.punto_pos + 1] == X:
                #print("Mover")
                simbolos_a_cambiar = ele_lr0.p_lista[ele_lr0.punto_pos], ele_lr0.p_lista[ele_lr0.punto_pos + 1]
                nueva_lista_lr0 = copy(ele_lr0.p_lista)
                nueva_lista_lr0[ele_lr0.punto_pos + 1], nueva_lista_lr0[ele_lr0.punto_pos] = simbolos_a_cambiar

                subconjunto_mover.add(ElementoLR0(ele_lr0.no_terminal, lista_a_str(nueva_lista_lr0), nueva_lista_lr0, ele_lr0.punto_pos + 1, ele_lr0.num_produccion))

    """if len(subconjunto_mover) > 0:

        print(f'\nMover con {X}')
        for lr0 in subconjunto_mover:
            print(f"{lr0.no_terminal} -> {lr0.p_cadena}")
    """

    return subconjunto_mover



class TablaLR0:
    def __init__(self):
        self.filas = dict()

    def mover_conjunto_simbolos(self, gic, is_terminales, subconjuntos, i_subconjunto, conteo_subconjuntos):
        """
        Calcula Mover de los subconjuntos encontrados y los símbolos de la gramática.
        is_terminales: Define si se está moviendo con terminales o no terminales.
        """

        if is_terminales:
            conjunto_simbolos = gic.terminales
        else:
            conjunto_simbolos = gic.no_terminales

        for simbolo in conjunto_simbolos:
            kernel = mover(subconjuntos[i_subconjunto].elementos_LR0, simbolo)
            if len(kernel) > 0:
                kernel_str = set()
                for ele_lr0 in kernel:
                    kernel_str.add(f'{ele_lr0.no_terminal} -> {ele_lr0.p_cadena}')
                
                sub_existe = False
                numero_subconjunto_previo = -1
                for subconjunto in subconjuntos:
                    if subconjunto.kernel == kernel_str:
                        sub_existe = True
                        numero_subconjunto_previo = subconjunto.numero
                        break

                if simbolo not in self.filas[subconjuntos[i_subconjunto].numero].keys():
                    self.filas[subconjuntos[i_subconjunto].numero][simbolo] = []                        

                if is_terminales:
                    if not sub_existe:
                        conteo_subconjuntos += 1
                        subconjuntos.append(SubconjuntoLR0(kernel_str, cerradura(kernel, gic), conteo_subconjuntos))
                        self.filas[subconjuntos[i_subconjunto].numero][simbolo].append('d'+str(conteo_subconjuntos))
                    else:
                        self.filas[subconjuntos[i_subconjunto].numero][simbolo].append('d'+str(numero_subconjunto_previo))

                else:
                    if not sub_existe:
                        conteo_subconjuntos += 1
                        subconjuntos.append(SubconjuntoLR0(kernel_str, cerradura(kernel, gic), conteo_subconjuntos))
                        self.filas[subconjuntos[i_subconjunto].numero][simbolo] = [conteo_subconjuntos]
                    else:
                        self.filas[subconjuntos[i_subconjunto].numero][simbolo] = [numero_subconjunto_previo]

        return conteo_subconjuntos       

    def llenar(self, gic):

        #print("--------------------------------------------")
        # Extendiendo la gramática.
        n_term_extendido = gic.inicial + "'"
        is_repetido = False
        if n_term_extendido in gic.no_terminales:
            is_repetido = True
            #print("Ya está")
        
        while is_repetido:
            n_term_extendido += "'"
            if n_term_extendido not in gic.no_terminales:
                is_repetido = False

        elemento_inicial = ElementoLR0(n_term_extendido, f'. {gic.inicial}', ['.', gic.inicial], 0, -1)
        #print("--------------------------------------------")

        subconjunto_0 = set()
        subconjunto_0.add(elemento_inicial)

        subconjunto = cerradura(subconjunto_0, gic)
        #print("-----------",subconjunto)

        subconjuntos = [SubconjuntoLR0(set(), subconjunto, 1)]

        i_subconjunto = 0
        conteo_subconjuntos = 1

        while i_subconjunto < len(subconjuntos):

            if subconjuntos[i_subconjunto].numero not in self.filas.keys():
                self.filas[subconjuntos[i_subconjunto].numero] = {}

            conteo_subconjuntos = self.mover_conjunto_simbolos(gic, False, subconjuntos, i_subconjunto, conteo_subconjuntos)
            conteo_subconjuntos = self.mover_conjunto_simbolos(gic, True, subconjuntos, i_subconjunto, conteo_subconjuntos)

            i_subconjunto += 1  

        for subconjunto in subconjuntos:
            #print(f" {subconjunto.numero}) {subconjunto.kernel}")
            #print(subconjunto.elementos_LR0)
            for lr0 in subconjunto.elementos_LR0:
                if lr0.punto_pos == len(lr0.p_lista) - 1:
                    #print(f"Final: {lr0.num_produccion}) {lr0.no_terminal} -> {lr0.p_cadena}")
                    if lr0.num_produccion == -1 and f"{gic.inicial} . " == lr0.p_cadena:
                        
                        self.filas[subconjunto.numero]['$'] = ['acc']
                    else:
                        #print(f'Siguiente({lr0.no_terminal}) = {gic.siguiente(lr0.no_terminal)}')

                        siguiente_no_terminal = gic.siguiente(lr0.no_terminal)
                        #print(f"S({lr0.no_terminal}) = {siguiente_no_terminal} ")
                        for sig in siguiente_no_terminal:
                            if sig not in self.filas[subconjunto.numero].keys():
                                self.filas[subconjunto.numero][sig] = []
                                #print(f"No existe: {subconjunto.numero} {sig}")
                            self.filas[subconjunto.numero][sig].append('r'+str(lr0.num_produccion))

        #for sub in self.filas.keys():
        #    print(f"{sub}) {self.filas[sub]}")

        self.subconjuntos = subconjuntos

    def imprimir(self, gic):
        
        print(f'{"" : <7} {gic.terminales[0] : <4}', end='')
        if len(gic.terminales) > 1:
            for terminal in gic.terminales[1:]:
                print(f'    {terminal : <4}', end='')
            print(f'    {"$" : <4}', end='')

        print(f'{"" : <7} {gic.no_terminales[0] : <4}', end='')
        if len(gic.no_terminales) > 1:
            for no_terminal in gic.no_terminales[1:]:
                print(f'    {no_terminal : <4}', end='')
            print()

        for subconjunto in self.subconjuntos:
            print(f'{subconjunto.numero : <8}', end='')

            for terminal in gic.terminales:
                if terminal in self.filas[subconjunto.numero].keys():
                    acciones_str = lista_a_str(self.filas[subconjunto.numero][terminal])
                    print(f'{acciones_str : <8}', end='')
                else:
                    print(f'{"" : <8}', end='')

            if '$' in self.filas[subconjunto.numero].keys():
                acciones_str = lista_a_str(self.filas[subconjunto.numero]['$'])
                print(f'{acciones_str : <8}', end='')
            else:
                print(f'{"" : <12}', end='')

            for no_terminal in gic.no_terminales:
                if no_terminal in self.filas[subconjunto.numero].keys():
                    acciones_str = lista_num_a_str(self.filas[subconjunto.numero][no_terminal])
                    print(f'{acciones_str : <8}', end='')
                else:
                    print(f'{"" : <8}', end='')

            print()                            

    def analisis_LR0(self, gic, entrada):
        
        #print(type(self.subconjuntos))

        #for subconjunto in self.subconjuntos:
        #    print(subconjunto.numero)

        print()
        print("Análisis LR(0)")

        entrada_extendida = entrada.split()
        entrada_extendida.append('$')
        i_entrada = 0
        pila = [self.subconjuntos[0].numero]
        
        print(f"Cadena: {lista_a_str(entrada_extendida)}")

        #print(pila[0])
        
        while True:
            #print("Pila: ", pila)
            #print("Cadena: ", entrada_extendida[i_entrada:])
            sim_cadena = entrada_extendida[i_entrada]
            if sim_cadena not in self.filas[pila[-1]]:
                print("Error. La cadena no pertenece a L(G).")
                return

            if len(self.filas[pila[-1]][sim_cadena]) > 1:
                print(self.filas[pila[-1]][sim_cadena])
                print("Entrada múltiple. No se puede determinar si la cadena pertenece o no a L(G).")
                return

            if self.filas[pila[-1]][sim_cadena][0][0] == 'd':
                #print("Desplazamiento")
                i_entrada += 1
                pila.append(int(self.filas[pila[-1]][sim_cadena][0][1:]))
            elif self.filas[pila[-1]][sim_cadena][0][0] == 'r':
                num_produccion = int(self.filas[pila[-1]][sim_cadena][0][1:])
                print(f"Reducción con {gic.producciones[num_produccion][0]} -> {lista_a_str(gic.producciones[num_produccion][1])} ")
                #print(f"{gic.producciones[num_produccion][0]} -> {gic.producciones[num_produccion][1]}")
                if not (len(gic.producciones[num_produccion][1]) == 1 and gic.producciones[num_produccion][1][0] == ''):
                    #print("No es E. :D")
                    for i in range(len(gic.producciones[num_produccion][1])):
                        pila.pop()
                pila.append(self.filas[pila[-1]][gic.producciones[num_produccion][0]][0])
                    
            elif self.filas[pila[-1]][sim_cadena][0] == 'acc':
                print("Cadena aceptada.")
                return

