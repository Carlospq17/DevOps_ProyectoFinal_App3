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
        result = c.executeQuery(connection, "SHOW TABLES")
        for row in result:
            print(row[0])
        return

if __name__ == "__main__":
    m = main()
    m.backup()