
class FileWriter:

    _filename = "testfile.txt"

    def __init__(self, filename):
        if filename != '':
            self._filename = filename

    def writeFile(self, object):
        file = open(self._filename, "w")
        file.write(str(object))
        file.close()
