import logging
import json

class JSONHandler:

    def __init__(self):
        return

    def getJSON(self, filename):
        try:
            f = open(filename)
            j = json.load(f)
            return j
        except ValueError:
            logging.warning("El archivo que intenta acceder está vacío")
            self.writeJSON(filename + ".json", "{}")
            return 0
        except FileNotFoundError:
            logging.error("El archivo que intenta acceder no existe")
            self.writeJSON( filename + ".json", "{}")
            return 1

    def writeJSON(self, filename, data):
        logging.debug("Escribiendo: " + str(data) + " en el archivo: " + filename)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return

    def keyExists(self, json_string, string):
        a_dictionary = json.loads(json_string)
        b_in_dict =  string in a_dictionary
        logging.debug("La cadena: " + string + " es llave del json: " + str(json_string) + " = " + str(b_in_dict))
        return b_in_dict