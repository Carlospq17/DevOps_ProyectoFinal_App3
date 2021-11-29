from DBConnection import DBConnection
from File import File
import re

class main:
    def __init__(self):
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
            print(" === " + table[0] + " === ")
            tablesHeader = c.executeQuery(connection, "SHOW COLUMNS FROM " + table[0] + ";")
            tableColumnNames = []
            for tableHeader in tablesHeader:
                tableColumnNames.append(tableHeader[0])
                columnNames = ",".join(tableColumnNames)
            #print(columnNames)
            f.appendLineFile(table[0], columnNames)

            tablesBody = c.executeQuery(connection, "SELECT * FROM " + table[0] + ";")
            for tableRow in tablesBody:
                rowElementList = []
                for rowElements in tableRow:
                    rowElementList.append(rowElements)
                columnValues = ','.join(map(str, rowElementList))
                #print(columnValues)
                f.appendLineFile(table[0], columnValues)

        return

if __name__ == "__main__":
    m = main()
    m.backup()