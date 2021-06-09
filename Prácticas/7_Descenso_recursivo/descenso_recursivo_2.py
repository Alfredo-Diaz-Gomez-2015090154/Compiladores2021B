cadena = input('Ingresa la cadena a probar: ')
#cadena = "abababbccaaaaacaaac"
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
    if consumir('a'):
        if consumir('b'):
            if S():
                return A()
        return False
    elif consumir('b'):
        return A()

def A():
    if consumir('a'):
        return A()
    elif consumir('c'):
        return True
    return False

def main():

    global indice_actual

    try:
        S()
    except:
        aciertos = -1

    if indice_actual == longitud_cadena:
        print("Aceptada.")
    else:
        print("No aceptada.")

if __name__ == "__main__":
    main()
