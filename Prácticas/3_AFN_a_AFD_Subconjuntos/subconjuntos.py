import copy
from AFD import AFD
from Estado import Estado


def mover(estados_E, c, tabla_referencia):

    kernel = []

    if c in tabla_referencia.keys():
        for e in estados_E:
            if e in tabla_referencia[c].keys():
                kernel.extend(tabla_referencia[c][e])
    
    return kernel

def calcular_cerradura_E(kernel, AFND_entrada):

    cerradura_E_resultante = copy.copy(kernel)
    cont_pos_cE = 0
    while cont_pos_cE < len(cerradura_E_resultante):
        if (cerradura_E_resultante[cont_pos_cE], 'E') in AFND_entrada.transiciones.keys():
            for e in AFND_entrada.transiciones[(cerradura_E_resultante[cont_pos_cE], 'E')]:
                if e not in cerradura_E_resultante:
                    cerradura_E_resultante.append(e)
        cont_pos_cE += 1
    return cerradura_E_resultante

def AFND_a_AFD(AFND_entrada):

    AFD_resultado = AFD(AFND_entrada.alfabeto)

    tabla_referencia = {}
    for transicion_AFN in AFND_entrada.transiciones.keys():
        if transicion_AFN[1] not in tabla_referencia.keys():
            tabla_referencia[transicion_AFN[1]] = {}
        tabla_referencia[transicion_AFN[1]][transicion_AFN[0]] =  AFND_entrada.transiciones[transicion_AFN]
    
    #print(tabla_referencia)

    #Cálculo de cerradura-E. Se empieza con el estado inicial y a partir de ahí se obtienen los estados
    #a los que se puede llegar utilizando E.
    cerradura_E = [AFND_entrada.estado_inicial]
    cont_pos_cE = 0
    while cont_pos_cE < len(cerradura_E):
        if (cerradura_E[cont_pos_cE], 'E') in AFND_entrada.transiciones.keys():
            for e in AFND_entrada.transiciones[(cerradura_E[cont_pos_cE], 'E')]:
                if e not in cerradura_E:
                    cerradura_E.append(e)
        cont_pos_cE += 1

    inicial = Estado('A_0', None, cerradura_E)
    estados_AFD = []
    cola_estados = [inicial]

    contador_letra_estado = 66
    contador_vueltas_alfabeto = 0

    while len(cola_estados) != 0:
        for c in AFND_entrada.alfabeto:
            kernel_estado = mover(cola_estados[0].estados_AFND, c, tabla_referencia)
            #print(f"{c} : {kernel_estado}")

            estado_kernel_igual = None
            for estado_generado in estados_AFD:
                if kernel_estado == estado_generado.kernel:
                    estado_kernel_igual = estado_generado
                    break
            
            if estado_kernel_igual is not None:
                AFD_resultado.agregar_estado(cola_estados[0].nombre, c, estado_kernel_igual.nombre)
            else:
                cerradura_E_resultante = calcular_cerradura_E(kernel_estado, AFND_entrada)
                #print(cerradura_E_resultante)
                if contador_letra_estado == 91:
                    contador_letra_estado = 65
                    contador_vueltas_alfabeto += 1
                nuevo_estado = Estado(f"{chr(contador_letra_estado)}_{contador_vueltas_alfabeto}", kernel_estado, cerradura_E_resultante)
                estados_AFD.append(nuevo_estado)
                cola_estados.append(nuevo_estado)
                AFD_resultado.agregar_estado(cola_estados[0].nombre, c, nuevo_estado.nombre)
                contador_letra_estado += 1

                #Se verifica si se encontró un estado pozo.
                if kernel_estado == []:
                    AFD_resultado.determinar_estado_pozo(nuevo_estado.nombre)

        
        cola_estados.pop(0)
    
    #Obtención de nombres de estados.
    nombres_estados = [inicial.nombre] + [estado.nombre for estado in estados_AFD]
    AFD_resultado.copiar_estados(nombres_estados)

    #Selección del estado inicial.
    AFD_resultado.copiar_estado_inicial(inicial.nombre)

    #Selección de estados finales.
    AFD_finales = []
    for final_afnd in AFND_entrada.estados_finales:
        if final_afnd in inicial.estados_AFND:
            AFD_finales.append(inicial.nombre)
            break
    for estado in estados_AFD:
        for final_afnd in AFND_entrada.estados_finales:
            if final_afnd in estado.estados_AFND:
                AFD_finales.append(estado.nombre)
                break
    AFD_resultado.copiar_estados_finales(AFD_finales)


    return AFD_resultado

    

