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
            print("El archivo que intenta acceder está vacío")
            return 0
        except FileNotFoundError:
            print("El archivo que intenta acceder no existe")
            return 1

    def writeJSON(self, filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return

    def keyExists(self, json_string, string):
        a_dictionary = json.loads(json_string)
        b_in_dict =  string in a_dictionary
        return b_in_dict