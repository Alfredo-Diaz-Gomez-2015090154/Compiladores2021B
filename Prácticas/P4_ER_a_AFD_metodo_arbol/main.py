from Util import Util
from metodo_arbol import construir_arbol, construir_tabla_siguientes
from afd import Estado, AFD


def main():

    er = input("Expresión regular: ")
    er_filtrada = Util.filtrar_er(er)
    if er_filtrada == -1:
        print("Error en expresión regular")
        return
    posfija = Util.infija_a_posfija(er_filtrada)
    # print(posfija+'#.')
    nodo_raiz, no_simbolos, simbolos_orden = construir_arbol(posfija+'#.')
    tabla_siguientes = construir_tabla_siguientes(nodo_raiz, no_simbolos)

    # print(simbolos_orden)

    nodo_raiz.primera.sort()
    # print(f"Primeraaaaa: {nodo_raiz.primera}")

    # print(nodo_raiz.primera)

    nombre_estado_inicial = ''
    for indice_estado in nodo_raiz.primera[:-1]:
        # print(indice_estado)
        nombre_estado_inicial += f'{indice_estado}_'
    nombre_estado_inicial += f'{nodo_raiz.primera[-1]}'

    # print("NOmbreeeeeeeeeeee", nombre_estado_inicial)

    estado_inicial = Estado(nodo_raiz.primera, nombre_estado_inicial)
    # print(estado_inicial.nombre)

    AFD_resultante = AFD(estado_inicial, ('a', 'b', 'c'))

    AFD_resultante.construir_estados(tabla_siguientes, simbolos_orden)

    print("AFD: ")
    print(f'Alfabeto: {AFD_resultante.alfabeto}')
    print(f'Estados: ')
    for estado in AFD_resultante.estados:
        print(estado.nombre)
    print(f'Estado inicial: {AFD_resultante.estado_inicial.nombre}')
    print('Estados finales: ')
    for estado_final in AFD_resultante.estados_finales:
        print(estado_final)
    print('Transiciones: ')
    for transicion in AFD_resultante.transiciones.keys():
        print(f'{transicion} -> {AFD_resultante.transiciones[transicion]}')

if __name__ == "__main__":
    main()