from os import system, mkdir
from os.path import isdir
from AFND import AFND

class Util_thompson:

    @staticmethod
    def filtrar_er(cadena_er):

        alfabeto = []

        if len(cadena_er) == 0:
            return -1, None

        contador_parentesis = 0

        er_filtrada = ''
        if cadena_er[0] == '*' or cadena_er[0] == ')' or cadena_er[0] == '|':
            #print("Incorrecto primer caracter.")
            return -1, None 

        er_filtrada += cadena_er[0]
        if cadena_er[0] == '(':
            contador_parentesis += 1
            #print("Contador: ", contador_parentesis)
        elif cadena_er[0].islower():
            alfabeto.append(cadena_er[0])

        for c in cadena_er[1:]:

            #if c in alfabeto:
            if c.islower():

                if c not in alfabeto:
                    alfabeto.append(c)

                if er_filtrada[-1] == 'E':
                    #print("Incorrecto alfabeto.")
                    return -1, None 
                
                #if er_filtrada[-1] in alfabeto or er_filtrada[-1] == '*' or er_filtrada[-1] == ')':
                if er_filtrada[-1].islower() or er_filtrada[-1] == '*' or er_filtrada[-1] == ')':
                    er_filtrada += '.'
                er_filtrada += c

            elif c == '(':
                if er_filtrada[-1] == 'E':
                    #print("Incorrecto (")
                    return -1, None 
                
                contador_parentesis += 1
                #print("Contador: ", contador_parentesis)
                #if er_filtrada[-1] in alfabeto or er_filtrada[-1] == '*' or er_filtrada[-1] == ')':
                if er_filtrada[-1].islower() or er_filtrada[-1] == '*' or er_filtrada[-1] == ')':
                    er_filtrada += '.'
                er_filtrada += c
            
            elif c == ')':
                if er_filtrada[-1] == '|' or er_filtrada[-1] == '(':
                    #print("Incorrecto )")
                    return -1, None

                contador_parentesis -= 1
                #print("Contador: ", contador_parentesis)
                if contador_parentesis < 0:
                    #print("Paréntesis extra.")
                    return -1, None
                er_filtrada += c

            elif c == '*':
                if er_filtrada[-1] == '|' or er_filtrada[-1] == 'E' or er_filtrada[-1] == '(' or er_filtrada[-1] == '*':
                    #print("Incorrecto *")
                    return -1, None
                er_filtrada += c

            elif c == '|':
                if er_filtrada[-1] == '|' or er_filtrada[-1] == '(':
                    #print("Incorrecto |")
                    return -1, None
                er_filtrada += c

            elif c == 'E':
                #if er_filtrada[-1] in alfabeto or er_filtrada[-1] == '*' or er_filtrada[-1] == ')' or er_filtrada[-1] == 'E':
                if er_filtrada[-1].islower() or er_filtrada[-1] == '*' or er_filtrada[-1] == ')' or er_filtrada[-1] == 'E':
                    #print("Incorrecto E")
                    return -1, None
                er_filtrada += c
            else:
                #print("Incorrecto sin símbolo")
                return -1, None
        
        #print("Contador: ", contador_parentesis)
        if contador_parentesis != 0:
            #print("Paréntesis ( extra")
            return -1, None

        return er_filtrada, tuple(alfabeto)

    @staticmethod
    def infija_a_posfija(er, alfabeto):

        pila = []

        expresion_posfija = ''

        for c in er:
            if c in alfabeto:
                expresion_posfija += c

            elif c == 'E':
                expresion_posfija += c

            elif c == '(':
                pila.append('(')

            elif c == ')':
                while len(pila) > 0 and pila[-1] != '(':
                    expresion_posfija += pila[-1]
                    pila.pop()
                if pila[-1] == '(':
                    pila.pop()

            elif c == '*':
                if len(pila) > 0:
                    while len(pila) > 0 and pila[-1] == '*':
                        expresion_posfija += pila[-1]
                        pila.pop()
                    pila.append('*') 
                else:
                    pila.append('*')

            elif c == '.':
                if len(pila) > 0:
                    while len(pila) > 0 and (pila[-1] == '*' or pila[-1] == '.'):
                        expresion_posfija += pila[-1]
                        pila.pop()
                    pila.append('.')
                else:
                    pila.append('.')

            elif c == '|':
                if len(pila) > 0:
                    while len(pila) > 0 and (pila[-1] == '*' or pila[-1] == '.' or pila[-1] == '|'):
                        expresion_posfija += pila[-1]
                        pila.pop()
                    pila.append('|')
                else:
                    pila.append('|')
        
        while len(pila) != 0:
            expresion_posfija += pila[-1]
            pila.pop()

        return expresion_posfija          

    @staticmethod
    def evaluar_er_posfija(posfija, alfabeto):

        pila = []
        contadores_ocurrencias = {}
        contador_r = 0
        contador_E = 0

        AFND.alfabeto = alfabeto

        for c in posfija:

            if c in alfabeto:
                if c not in contadores_ocurrencias.keys():
                    contadores_ocurrencias[c] = 1
                else:
                    contadores_ocurrencias[c] += 1

                pila.append(AFND.unitaria(c, contadores_ocurrencias[c]))

            elif c == 'E':
                contador_E += 1
                pila.append(AFND.epsilon(contador_E))
            
            elif c == '*':
                contador_r += 1
                aux = pila[-1]
                pila.pop()
                pila.append(AFND.estrella(aux, contador_r))
            
            elif c == '.':
                contador_r += 1
                aux_2 = pila[-1]
                pila.pop()
                aux_1 = pila[-1]
                pila.pop()
                pila.append(AFND.concatenacion(aux_1, aux_2, contador_r))

            elif c == '|':
                contador_r += 1
                aux_2 = pila[-1]
                pila.pop()
                aux_1 = pila[-1]
                pila.pop()
                pila.append(AFND.union(aux_1, aux_2, contador_r))

        return pila[-1]    

    # dot -Tpng <archivo>.gv -o <salida>.png
    # dot -Tpng graficos/afnd.gv -o graficos/resultado.png
    @staticmethod
    def dibujar_AFND(afnd):

        if not isdir('graficos'):
            mkdir('graficos')

        with open('graficos/afnd.gv', 'w') as file:

            file.write('digraph G {\n')
            file.write(' rankdir=LR;\n')
            file.write(' I [ label = "I", style = invis];\n')

            for estado in afnd.estados:
                if estado in afnd.finales:
                    file.write(f' {estado} [ shape = doublecircle ];\n')
                else:
                    file.write(f' {estado} [ shape = circle ];\n')

            file.write(f' I -> {afnd.estado_inicial};\n')

            for llave in afnd.transiciones.keys():
                for transicion in afnd.transiciones[llave]:
                    if llave[1] == '':
                        file.write(f' {llave[0]} -> {transicion} [ label = "E"]; \n')
                    else:
                        file.write(f' {llave[0]} -> {transicion} [ label = "{llave[1]}"]; \n')
                    
            file.write("}")

        system("dot -Tpng graficos/afnd.gv -o graficos/resultado.png")
