from AFND import AFND
from Util_thompson import Util_thompson

def main():

    er = input("Expresión regular: ")
    er_filtrada, alfabeto = Util_thompson.filtrar_er(er)
    if er_filtrada == -1:
        print("Error en expresión regular")
        return
    
    posfija = Util_thompson.infija_a_posfija(er_filtrada, alfabeto)
    print(posfija)

    AFND_final = Util_thompson.evaluar_er_posfija(posfija, alfabeto)    
    AFND_final.numerar_estados()
    AFND_final.mostrar_informacion()

    Util_thompson.dibujar_AFND(AFND_final)
    AFND_final.afnd_json()
    return

if __name__ == "__main__":
    main()
