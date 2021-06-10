cadena = input('Ingresa la cadena a probar: ')
longitud_cadena = len(cadena)
aciertos = 0
indice_actual = 0

def A():
    global indice_actual
    global cadena
    global aciertos

    #Consume a.
    if cadena[indice_actual] == 'a':
        aciertos += 1
    indice_actual += 1
    
    #No terminal B.
    B()

    #Consume a.
    if cadena[indice_actual] == 'a':
        aciertos += 1
    indice_actual += 1
    

def B():
    global indice_actual
    global cadena 
    global aciertos

    #Consume c.
    if cadena[indice_actual] == 'c':
        aciertos += 1
        indice_actual += 1
        return
    
    #Consume b.
    if cadena[indice_actual] == 'b':
        aciertos += 1
    indice_actual += 1

    #No terminal A.
    A()

    #Consume b.
    if cadena[indice_actual] == 'b':
        aciertos += 1
    indice_actual += 1
    

def main():

    global indice_actual
    global aciertos

    try:
        A()
    except:
        aciertos = -1


    if aciertos == longitud_cadena:
        print("La cadena SÍ pertenece al lenguaje.")
    else:
        print("La cadena NO pertenece al lenguaje.")

if __name__ == "__main__":
    main()
