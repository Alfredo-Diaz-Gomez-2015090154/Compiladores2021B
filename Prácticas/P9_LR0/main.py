#from Prácticas.P9_LR0.LR0 import SubconjuntoLR0
from GIC import GIC
from LR0 import cerradura, mover, ElementoLR0, SubconjuntoLR0, TablaLR0

def main():

    #Ejemplo 1:
    """no_terminales = ["E", "E'", "T", "T'", "F"]
    terminales = ['+', '*', '(', ')', 'id']
    producciones = [
        ('E', ['T', "E'"]), 
        ("E'", ['+', 'T', "E'"]), ("E'", ['']),
        ("T", ['F', "T'"]), 
        ("T'", ['*', 'F', "T'"]), ("T'", ['']),
        ("F", ['(', 'E', ')']), ("F", ['id']),
        ]
    inicial = 'E'
    cadena = '( id + id * id ) + id'"""
    

    #Ejemplo 2:
    no_terminales = ['S', 'A', 'B']
    terminales = ['1', '0']
    producciones = [
        ('S', ['A', '1', 'B']),
        ('A', ['0', 'A']),
        ('A', ['']),
        ('B', ['0', 'B']),
        ('B', ['1', 'B']),
        ('B', ['']),
    ]
    inicial = 'S'
    cadena = '0 1 1 1'
    

    # Ejemplo 3
    """no_terminales = ['S', 'A', 'B', 'D']
    terminales = ['a', 'b', 'd']
    producciones = [
        ('S', ['A', 'a']),
        ('A', ['B', 'D']),
        ('B', ['b']),
        ('B', ['']),
        ('D', ['d']),
        ('D', [''])
    ]
    inicial = 'S'
    cadena = 'b d'"""

    # Ejemplo 4
    """no_terminales = ['S', 'X']
    terminales = ['x', 'y']
    producciones = [
        ('S', ['X', 'X']),
        ('X', ['x', 'X']),
        ('X', ['y'])
    ]
    inicial = 'S'
    cadena = 'x x x y x x x y' """

    # Ejemplo 5
    """no_terminales = ['S', 'X']
    terminales = ['0', '1']
    producciones = [
        ('S', ['X', '1', 'X', '1', 'X', '1', 'X']),
        ('X', ['0', 'X']),
        ('X', ['1', 'X']),
        ('X', [''])
    ]
    inicial = 'S'
    cadena = '1 1 1'"""
    

    # Ejemplo 6
    """no_terminales = ['E', 'T', 'F']
    terminales = ['+', '*', '(', ')', 'id']
    producciones = [
        ('E', ['E', '+', 'T']),
        ('E', ['T']),
        ('T', ['T', '*', 'F']),
        ('T', ['F']),
        ('F', ['(', 'E', ')']),
        ('F', ['id']),
    ]
    inicial = 'E'
    cadena = 'id'"""

    # Ejemplo 7
    """no_terminales = ['E', 'T', 'F']
    terminales = ['+', '*', '(', ')', 'id']
    producciones = [
        ('E', ['E', '+', 'T']),
        ('E', ['T']),
        ('T', ['T', '*', 'F']),
        ('T', ['F']),
        ('F', ['(', 'E', ')']),
        ('F', ['id']),
    ]
    inicial = 'E'
    cadena = 'id'"""

    gic = GIC(terminales, no_terminales, inicial, producciones)

    print("Gramática: ")
    gic.imprimir()

    tablaLR0 = TablaLR0()
    tablaLR0.llenar(gic)

    print()
    print("Tabla LR(0): ")
    tablaLR0.imprimir(gic)

    for subconjunto in tablaLR0.subconjuntos:
        print(f'{subconjunto.numero})  ', end='')
        for elemento in subconjunto.elementos_LR0:
            print(f'{elemento.no_terminal} -> {elemento.p_cadena}  ', end='')
        print()


if __name__ == "__main__":
    main()
