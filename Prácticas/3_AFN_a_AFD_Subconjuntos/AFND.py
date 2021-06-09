import json, copy

class AFND:

    def __init__(self, archivo_json):

        with open(archivo_json) as archivo_json_f:
            datos_json = json.load(archivo_json_f)

        self.alfabeto = tuple(datos_json["alfabeto"])
        self.estados = tuple(datos_json["estados"])
        self.estado_inicial = datos_json["estado_inicial"]
        self.estados_finales = tuple(datos_json["estados_finales"])
        self.transiciones = {}

        for keys in datos_json["transiciones"].keys():
            temp_transicion = keys.split(', ')
            self.transiciones[(int(temp_transicion[0][1:]), temp_transicion[1][:-1])] = datos_json["transiciones"][keys]
        

    def __str__(self):
        return f"""alfabeto : {self.alfabeto},
                estados : {self.estados},
                estado inicial : {self.estado_inicial},
                estados finales: {self.estados_finales},
                transiciones : {self.transiciones}"""