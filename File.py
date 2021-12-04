import logging

class File:

    def __init__(self):
        return

    def getArrayInfo(self, filepath):
        info = []
        f = open(filepath, "r")
        for x in f:
            info.append(x)
        f.close();
        logging.debug('Obteniendo los datos del archivo ' + filepath)
        logging.debug(info)
        return info

    def appendLineFile(self, filename, line):
        logging.debug('Escribiendo en archivo: ' + filename + ' los datos: ' + line)
        with open(filename, "a") as file:
            file.write(line + "\n")
        file.close()
        return
            

