from os import system, mkdir
from os.path import isdir

class Util_subconjuntos:

    @staticmethod
    def dibujar_AFD(afd):

        if not isdir('graficos'):
            mkdir('graficos')

        with open('graficos/afd.gv', 'w') as file:

            file.write('digraph G {\n')
            file.write(' rankdir=LR;\n')
            file.write(' I [ label = "I", style = invis];\n')

            for estado in afd.estados:
                if estado != afd.estado_pozo:
                    if estado in afd.estados_finales:
                        file.write(f' {estado} [ shape = doublecircle ];\n')
                    else:
                        file.write(f' {estado} [ shape = circle ];\n')

            file.write(f' I -> {afd.estado_inicial};\n')

            for llave in afd.transiciones.keys():
                if not afd.transiciones[llave] == afd.estado_pozo:
                    file.write(f' {llave[0]} -> {afd.transiciones[llave]} [ label = "{llave[1]}"]; \n')
                    
            file.write("}")

        system("dot -Tpng graficos/afd.gv -o graficos/resultado.png")