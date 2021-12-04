class File:

    def __init__(self):
        return

    def getArrayInfo(self, filepath):
        info = []
        f = open(filepath, "r")
        for x in f:
            info.append(x)
        f.close();
        return info

    def appendLineFile(self, filename, line):
        with open(filename, "a") as file:
            file.write(line + "\n")
        file.close()
            

