from nodos import Nodo, NoEpsilon, Hoja, Interno
from copy import copy


def construir_arbol(postfija):
    
    alfabeto = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
    
    pila = []
    contador_simbolo = 0
    simbolos_orden = []

    for elemento in postfija:

        if elemento in alfabeto or elemento == '#':
            contador_simbolo += 1
            pila.append(Hoja(contador_simbolo, elemento))
            simbolos_orden.append(elemento)
            

        elif elemento == 'E':
            pila.append(Nodo())
            pila[-1].is_anulable = True

        elif elemento == '|' or elemento == '.':
            # print(elemento)
            derecho = pila.pop()
            izquierdo = pila.pop()
            pila.append(Interno(elemento, izquierdo, derecho))

            if elemento == '|':
                if izquierdo.is_anulable or derecho.is_anulable:
                    pila[-1].is_anulable = True
                else:
                    pila[-1].is_anulable = False

                pila[-1].primera = list(set(izquierdo.primera) | set(derecho.primera))

                pila[-1].ultima = list(set(izquierdo.ultima) | set(derecho.ultima))

            else:
                if izquierdo.is_anulable and derecho.is_anulable:
                    pila[-1].is_anulable = True
                else:
                    pila[-1].is_anulable = False         

                if izquierdo.is_anulable:
                    pila[-1].primera = list(set(izquierdo.primera) | set(derecho.primera))
                else:
                    pila[-1].primera = copy(izquierdo.primera)

                if derecho.is_anulable:
                    pila[-1].ultima = list(set(izquierdo.ultima) | set(derecho.ultima))
                else:
                    pila[-1].ultima = copy(derecho.ultima)

            # print(pila[-1].primera)
            # print(pila[-1].ultima)

        elif elemento == '*':
            izquierdo = pila.pop()
            pila.append(Interno(elemento, izquierdo))
            pila[-1].is_anulable = True

            pila[-1].primera = copy(izquierdo.primera)
            pila[-1].ultima = copy(izquierdo.ultima)

            # print(pila[-1].primera)
            # print(pila[-1].ultima)

        else:
            return None

    # print("Pilaaaaaaaaaaaaaaaaa:")
    # print(pila[-1].primera)

    return pila[-1], contador_simbolo, simbolos_orden

def construir_tabla_siguientes(nodo_raiz, no_simbolos):

    tabla_siguientes = {}
    for i in range(1, no_simbolos+1):
        tabla_siguientes[i] = []

    nodo_raiz.postorden_tabla_siguiente(tabla_siguientes)

    # print(tabla_siguientes)
    return tabla_siguientes
