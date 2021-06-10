class Util:

    @staticmethod
    def filtrar_er(cadena_er):

        alfabeto = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
                'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')

        if len(cadena_er) == 0:
            return -1

        contador_parentesis = 0

        er_filtrada = ''
        if cadena_er[0] == '*' or cadena_er[0] == ')' or cadena_er[0] == '|':
            #print("Incorrecto primer caracter.")
            return -1

        er_filtrada += cadena_er[0]
        if cadena_er[0] == '(':
            contador_parentesis += 1
            #print("Contador: ", contador_parentesis)

        for c in cadena_er[1:]:

            if c in alfabeto:
                if er_filtrada[-1] == 'E':
                    #print("Incorrecto alfabeto.")
                    return -1
                
                if er_filtrada[-1] in alfabeto or er_filtrada[-1] == '*' or er_filtrada[-1] == ')':
                    er_filtrada += '.'
                er_filtrada += c

            elif c == '(':
                if er_filtrada[-1] == 'E':
                    #print("Incorrecto (")
                    return -1
                
                contador_parentesis += 1
                #print("Contador: ", contador_parentesis)
                if er_filtrada[-1] in alfabeto or er_filtrada[-1] == '*' or er_filtrada[-1] == ')':
                    er_filtrada += '.'
                er_filtrada += c
            
            elif c == ')':
                if er_filtrada[-1] == '|' or er_filtrada[-1] == '(':
                    #print("Incorrecto )")
                    return -1     

                contador_parentesis -= 1
                #print("Contador: ", contador_parentesis)
                if contador_parentesis < 0:
                    #print("Paréntesis extra.")
                    return -1       
                er_filtrada += c

            elif c == '*':
                if er_filtrada[-1] == '|' or er_filtrada[-1] == 'E' or er_filtrada[-1] == '(' or er_filtrada[-1] == '*':
                    #print("Incorrecto *")
                    return -1
                er_filtrada += c

            elif c == '|':
                if er_filtrada[-1] == '|' or er_filtrada[-1] == '(':
                    #print("Incorrecto |")
                    return -1
                er_filtrada += c

            elif c == 'E':
                if er_filtrada[-1] in alfabeto or er_filtrada[-1] == '*' or er_filtrada[-1] == ')' or er_filtrada[-1] == 'E':
                    #print("Incorrecto E")
                    return -1
                er_filtrada += c
            else:
                #print("Incorrecto sin símbolo")
                return -1
        
        #print("Contador: ", contador_parentesis)
        if contador_parentesis != 0:
            #print("Paréntesis ( extra")
            return -1

        return er_filtrada

    @staticmethod
    def infija_a_posfija(er):

        alfabeto = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
                'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')

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
