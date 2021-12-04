import re
import os
import glob
import datetime
from os import walk
from DBConnection import DBConnection
from File import File
from GoogleDriveConnection import GoogleDriveConnection

class main:

    __date = ""

    def __init__(self):
        self.__date = datetime.datetime.now()
        return
    
    def clear_directory(self):
        files = glob.glob('punto_de_venta/*')
        for f in files:
            os.remove(f)
        return

    def saveCSVinDrive(self):
        g = GoogleDriveConnection()
        for (dirpath, dirnames, filenames) in walk("punto_de_venta/"):
            for name in filenames:
                g.loadFileGoogleDrive(dirpath, name)
        g.generateNewSavedFilesJSON()
        return

    def buildDBProperties(self, info):
        properties = {}
        for l in info:
            e = l.split("=")
            v = re.search("(?<=\").*?(?=\")", l)
            o = {e[0] : v.group()}
            properties.update(o)
        return properties
    
    def backup(self):
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
            tableColumnNames = []
            for tableHeader in tablesHeader:
                tableColumnNames.append(tableHeader[0])
                columnNames = ','.join(map(str, tableColumnNames))
            f.appendLineFile( "punto_de_venta/" + table[0] + "_" + self.__date.strftime("%Y") + "-" + self.__date.strftime("%m") + "-" + self.__date.strftime("%d") + "-" + self.__date.strftime("%H") + ":" + self.__date.strftime("%M") + ".csv", columnNames)

            tablesBody = c.executeQuery(connection, "SELECT * FROM " + table[0] + ";")
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