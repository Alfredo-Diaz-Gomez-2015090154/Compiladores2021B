from copy import copy, deepcopy

class GIC:

    def __init__(self, terminales, no_terminales, inicial, producciones):
        self.terminales = copy(terminales)
        self.no_terminales = copy(no_terminales)
        self.inicial = inicial
        self.producciones = deepcopy(producciones)


    def imprimir(self):
        
        print(f'No terminales: {self.no_terminales}')
        print(f'Inicial: {self.inicial}')
        print(f'Terminales: {self.terminales}')
        
        print('Producciones: ')
        for i, produccion in enumerate(self.producciones):
            derecho = ''
            for simbolo in produccion[1]:
                derecho += str(simbolo) + ' '
            print(f'  {i}) {produccion[0]} -> {derecho}')
        

    def primero(self, X):
        '''
            Regla 1: X es Terminal.
            Regla 2: X es No Terminal.
            Regla 3: X -> épsilon
            Regla 4: "Algo parecido a la regla 2."
        '''

        conjunto_primero = set()

        if len(X) != 1:

            primero_x_k = set()
            for simbolo in X:
                primero_x_k = self.primero([simbolo])
                if not '' in primero_x_k:
                    conjunto_primero = conjunto_primero.union(primero_x_k)
                    return conjunto_primero
                else:
                    conjunto_primero = conjunto_primero.union(primero_x_k-{''})

            if '' in primero_x_k:
                conjunto_primero.add('')
            
            return conjunto_primero
            

        else:
            if X[0] in self.terminales or X[0] == '': # Regla 1 y 2
                return {X[0]}
            elif X[0] in self.no_terminales:
                for produccion in self.producciones:
                    if X[0] == produccion[0]:
                        if produccion[1][0] != X[0]:
                            conjunto_primero = conjunto_primero.union(self.primero(produccion[1]))

                return conjunto_primero

    def siguiente(self, no_terminal):

        conjunto_siguiente = set()

        if no_terminal == self.inicial:
            conjunto_siguiente.add('$')

        for produccion in self.producciones:
            
            indices_simbolo = [i for i, x in enumerate(produccion[1]) if x == no_terminal]
        
            if len(indices_simbolo) > 0:

                for i in indices_simbolo:

                    if i == len(produccion[1]) - 1:
                        if no_terminal != produccion[0]:    # Comprobar la recursión.
                            conjunto_siguiente = conjunto_siguiente.union(self.siguiente(produccion[0]))
                    else:
                        primero_beta = self.primero(produccion[1][i+1:])
                        
                        if '' in primero_beta:
                            conjunto_siguiente = conjunto_siguiente.union(primero_beta - {''})
                            if no_terminal != produccion[0]:    # Comprobar la recursión.
                                conjunto_siguiente = conjunto_siguiente.union(self.siguiente(produccion[0]))
                        else:
                            conjunto_siguiente = conjunto_siguiente.union(primero_beta)
                            conjunto_siguiente = conjunto_siguiente.union(primero_beta)

        return conjunto_siguiente