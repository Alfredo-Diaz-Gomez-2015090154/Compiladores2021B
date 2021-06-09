from AFND import AFND
from subconjuntos import AFND_a_AFD
from Util_subconjuntos import Util_subconjuntos

def main():

    AFND_1 = AFND("AFNDs/resultado.json")
    AFD_resultante = AFND_a_AFD(AFND_1)
    AFD_resultante.mostrar_elementos()
    Util_subconjuntos.dibujar_AFD(AFD_resultante)



if __name__ == "__main__":
    main()
