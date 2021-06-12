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

    def llenar(self, gic):

        elemento_inicial = ElementoLR0("S'", '. S ', ['.', 'S'], 0, -1)

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

            for no_terminal in gic.no_terminales:
                kernel = mover(subconjuntos[i_subconjunto].elementos_LR0, no_terminal)
                if len(kernel) > 0:
                    #print("Si pasa")
                    kernel_str = set()
                    for ele_lr0 in kernel:
                        kernel_str.add(f'{ele_lr0.no_terminal} -> {ele_lr0.p_cadena}')
                    
                    #print(kernel_str)
                    sub_existe = False
                    numero_subconjunto_previo = -1
                    for subconjunto in subconjuntos:
                        if subconjunto.kernel == kernel_str:
                            sub_existe = True
                            numero_subconjunto_previo = subconjunto.numero
                            break

                    if no_terminal not in self.filas[subconjuntos[i_subconjunto].numero].keys():
                        self.filas[subconjuntos[i_subconjunto].numero][no_terminal] = []                        

                    if not sub_existe:
                        conteo_subconjuntos += 1
                        #print(f"No existe. Calcular cerradura : {conteo_subconjuntos}")                    
                        subconjuntos.append(SubconjuntoLR0(kernel_str, cerradura(kernel, gic), conteo_subconjuntos))
                        
                        self.filas[subconjuntos[i_subconjunto].numero][no_terminal] = [conteo_subconjuntos]
                    else:
                        self.filas[subconjuntos[i_subconjunto].numero][no_terminal] = [numero_subconjunto_previo]

            for terminal in gic.terminales:
                kernel = mover(subconjuntos[i_subconjunto].elementos_LR0, terminal)
                if len(kernel) > 0:
                    #print("Si pasa")
                    kernel_str = set()
                    for ele_lr0 in kernel:
                        kernel_str.add(f'{ele_lr0.no_terminal} -> {ele_lr0.p_cadena}')
                    
                    #print(kernel_str)
                    sub_existe = False
                    numero_subconjunto_previo = -1
                    for subconjunto in subconjuntos:
                        if subconjunto.kernel == kernel_str:
                            numero_subconjunto_previo = subconjunto.numero
                            sub_existe = True
                            break

                    if terminal not in self.filas[subconjuntos[i_subconjunto].numero].keys():
                        self.filas[subconjuntos[i_subconjunto].numero][terminal] = []
                        print(f"NO existente: {i_subconjunto}, {terminal}")
                        print(self.filas[subconjuntos[i_subconjunto].numero][terminal])
                    else:
                        print("Existente: ")
                        print(self.filas[subconjuntos[i_subconjunto].numero][terminal])

                    if not sub_existe:
                        conteo_subconjuntos += 1
                        #print(f"No existe. Calcular cerradura : {conteo_subconjuntos}")
                        subconjuntos.append(SubconjuntoLR0(kernel_str, cerradura(kernel, gic), conteo_subconjuntos))
                        self.filas[subconjuntos[i_subconjunto].numero][terminal].append('d'+str(conteo_subconjuntos))
                    else:
                        self.filas[subconjuntos[i_subconjunto].numero][terminal].append('d'+str(numero_subconjunto_previo))                

            i_subconjunto += 1  

        for subconjunto in subconjuntos:
            #print(f" {subconjunto.numero}) {subconjunto.kernel}")
            #print(subconjunto.elementos_LR0)
            for lr0 in subconjunto.elementos_LR0:
                if lr0.punto_pos == len(lr0.p_lista) - 1:
                    #print(f"Final: {lr0.num_produccion}) {lr0.no_terminal} -> {lr0.p_cadena}")
                    if lr0.num_produccion == -1:
                        self.filas[subconjunto.numero]['$'] = 'acc'
                    else:
                        #print(f'Siguiente({lr0.no_terminal}) = {gic.siguiente(lr0.no_terminal)}')

                        siguiente_no_terminal = gic.siguiente(lr0.no_terminal)
                        print(f"S({lr0.no_terminal}) = {siguiente_no_terminal} ")
                        for sig in siguiente_no_terminal:
                            if sig not in self.filas[subconjunto.numero].keys():
                                self.filas[subconjunto.numero][sig] = []
                                print(f"No existe: {subconjunto.numero} {sig}")
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
