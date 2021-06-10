#cadena = input('Ingresa la cadena a probar: ')
#cadena = "afdea"
#cadena = "bcafdeadfdea"
#cadena = "acafdeadea"
cadena = "afcafdeadea"

longitud_cadena = len(cadena)
indice_actual = 0

def consumir(caracter):
    global indice_actual
    if indice_actual < longitud_cadena:
        if cadena[indice_actual] == caracter:
            indice_actual += 1
            return True
    return False

def A():
    if B():
        if C():
            if D():
                if E():
                    return consumir('a')
    
    return False

def B():
    if consumir('b'):
        if C():
            return D()
    return consumir('a')

def C():
    if consumir('c'):
        return A()
    return consumir('f')

def D():
    return consumir('d')

def E():
    return consumir('e')

def main():
    if A() and indice_actual == longitud_cadena:
        print("Cadena aceptada.")
    else:
        print("Cadena NO aceptada.")
    
if __name__ == "__main__":
    main()
    