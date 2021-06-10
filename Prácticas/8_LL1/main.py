from GIC import GIC
from LL1 import TablaLL1


def main():

    #Ejemplo 1:
    no_terminales = ["E", "E'", "T", "T'", "F"]
    terminales = ['+', '*', '(', ')', 'id']
    producciones = [
        ('E', ['T', "E'"]), 
        ("E'", ['+', 'T', "E'"]), ("E'", ['']),
        ("T", ['F', "T'"]), 
        ("T'", ['*', 'F', "T'"]), ("T'", ['']),
        ("F", ['(', 'E', ')']), ("F", ['id']),
        ]
    inicial = 'E'
    cadena = '( id + id * id ) + id'
    

    #Ejemplo 2:
    """no_terminales = ['S', 'A', 'B']
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
    cadena = '0 1 1 1'"""
    

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


    gic = GIC(terminales, no_terminales, inicial, producciones)
    
    tablall1 = TablaLL1(no_terminales, terminales)
    tablall1.llenar(gic)
    
    print("Gramática: ")
    gic.imprimir()
    
    print("\nTabla LL(1)")
    tablall1.imprimir(gic)
    

    print()

    resultado = tablall1.analisis_LL1(cadena.split(), gic)
    if resultado == 1:
        print(f'La cadena {cadena} SÍ pertenece al L(G).')
    elif resultado == 0:
        print(f'La cadena {cadena} NO pertenece al L(G).')
    elif resultado == -1:
        print(f'Entrada múltiple. No se puede concluir si la cadena "{cadena}" pertenece o no a L(G).')


if __name__ == "__main__":
    main()
