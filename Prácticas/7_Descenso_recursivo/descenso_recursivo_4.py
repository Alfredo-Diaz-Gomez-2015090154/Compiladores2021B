cadena = input('Ingresa la cadena a probar: ')

longitud_cadena = len(cadena)
indice_actual = 0

def consumir(caracter):
    global indice_actual
    if indice_actual < longitud_cadena:
        if cadena[indice_actual] == caracter:
            indice_actual += 1
            return True
    return False

def S():
    if A():
        if B():
            return True
        return C()
    return False
    
def A():
    return consumir('a')

def B():
    return consumir('b')

def C():
    return consumir('c')

def main():
    if S() and indice_actual == longitud_cadena:
        print("Cadena aceptada.")
    else:
        print("Cadena NO aceptada.")

if __name__ == "__main__":
    main()