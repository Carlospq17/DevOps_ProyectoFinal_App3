import re
import os
import glob
from os import walk
from DBConnection import DBConnection
from File import File
from GoogleDriveConnection import GoogleDriveConnection

class main:
    def __init__(self):
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
        self.clear_directory()
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
                columnNames = ",".join(tableColumnNames)
            f.appendLineFile( "punto_de_venta/" +table[0], columnNames)

            tablesBody = c.executeQuery(connection, "SELECT * FROM " + table[0] + ";")
            for tableRow in tablesBody:
                rowElementList = []
                for rowElements in tableRow:
                    rowElementList.append(rowElements)
                columnValues = ','.join(map(str, rowElementList))
                f.appendLineFile( "punto_de_venta/" + table[0], columnValues)

        self.saveCSVinDrive()
        return

if __name__ == "__main__":
    m = main()
    m.backup()