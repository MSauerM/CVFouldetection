from datetime import datetime

class FileWriter:

    _filename = "testfile"
    _output_path = None
    _full_path = None

    def __init__(self, filename):
        if filename != '':
            self._filename = filename

    def set_output_directory(self, path: str):
        self._output_path = path

    def writeFile(self, write_object):
        self._full_path = self._output_path + self._filename + self.getCurrentDateTimeString() + ".txt"
        file = open(self._full_path, "w")
        file.write(str(write_object))
        file.close()

    def getCurrentDateTimeString(self):
        currentDateTime = datetime.now()
        return currentDateTime.strftime("%d-%m-%y_%H-%M")
