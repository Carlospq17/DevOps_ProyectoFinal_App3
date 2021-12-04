import re
import os
import glob
import logging
import datetime
from os import walk
from DBConnection import DBConnection
from File import File
from GoogleDriveConnection import GoogleDriveConnection

class main:

    __date = ""

    def __init__(self):
        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', filename='loggin.log', level=logging.DEBUG)
        self.__date = datetime.datetime.now()
        return
    
    def clear_directory(self):
        logging.info('Limpiando el directorio de la base de datos')
        files = glob.glob('punto_de_venta/*')
        for f in files:
            logging.debug('Eliminando el archivo ' + f)
            os.remove(f)
        return

    def saveCSVinDrive(self):
        logging.info('Guardando los archivos CSV de las tablas en Google Drive')
        g = GoogleDriveConnection()
        for (dirpath, dirnames, filenames) in walk("punto_de_venta/"):
            for name in filenames:
                g.loadFileGoogleDrive(dirpath, name)
        g.generateNewSavedFilesJSON()
        return

    def buildDBProperties(self, info):
        logging.info('Obteniendo propiedades para la base de datos')
        properties = {}
        for l in info:
            e = l.split("=")
            v = re.search("(?<=\").*?(?=\")", l)
            o = {e[0] : v.group()}
            properties.update(o)
        return properties
    
    def backup(self):
        logging.info('Realizando respaldo de tablas de la base de datos')
        f = File()
        info = f.getArrayInfo("database_properties.txt")
        properties = self.buildDBProperties(info)

        c = DBConnection(
            properties["host"],
            properties["database"],
            properties["user"],
            properties["password"]
            )

        connection = c.getMySQLConnection()
        tables = c.executeQuery(connection, "SHOW TABLES")

        for table in tables:
            tablesHeader = c.executeQuery(connection, "SHOW COLUMNS FROM " + table[0] + ";")
            logging.debug("Columnas de las tablas: " + str(tablesHeader))
            tableColumnNames = []
            for tableHeader in tablesHeader:
                tableColumnNames.append(tableHeader[0])
                columnNames = ','.join(map(str, tableColumnNames))
            f.appendLineFile( "punto_de_venta/" + table[0] + "_" + self.__date.strftime("%Y") + "-" + self.__date.strftime("%m") + "-" + self.__date.strftime("%d") + "-" + self.__date.strftime("%H") + ":" + self.__date.strftime("%M") + ".csv", columnNames)

            tablesBody = c.executeQuery(connection, "SELECT * FROM " + table[0] + ";")
            logging.debug('Información de las tablas: ' + str(tablesBody))
            for tableRow in tablesBody:
                rowElementList = []
                for rowElements in tableRow:
                    rowElements = rowElements.replace(",", "-") if isinstance(rowElements, str) else rowElements
                    rowElements = rowElements.replace("\n", " ") if isinstance(rowElements, str) else rowElements
                    rowElementList.append(rowElements)
                columnValues = ','.join(map(str, rowElementList))
                f.appendLineFile( "punto_de_venta/" + table[0] + "_" + self.__date.strftime("%Y") + "-" + self.__date.strftime("%m") + "-" + self.__date.strftime("%d") + "-" + self.__date.strftime("%H") + ":" + self.__date.strftime("%M") + ".csv", columnValues)
        return

if __name__ == "__main__":
    m = main()
    m.clear_directory()
    m.backup()
    m.saveCSVinDrive()