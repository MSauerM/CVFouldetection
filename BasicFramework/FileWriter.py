from datetime import datetime


class FileWriter:
    """
    Class for writing information of an object to an output text file
    ......

    Attributes
    -----------------
        _filename
            name of the file
        _output_path
            output directory for the output file
        _full_path
            the complete path of the output file

    Methods
    -----------------
        set_output_directory (path)
            specifies destination directory/path of the output file
        write_file (write_object)
            write information of the parameter object to a file unter the given full path
        get_current_date_time_string()
            returns curent date time in %d-%m-%y_%H-%M format
    """

    _filename = "testfile"
    _output_path = None
    _full_path = None

    def __init__(self, filename):
        if filename != '':
            self._filename = filename

    def set_output_directory(self, path: str):
        self._output_path = path

    def write_file(self, write_object):
        self._full_path = self._output_path + self._filename + self.get_current_date_time_string() + ".txt"
        file = open(self._full_path, "w")
        file.write(str(write_object))
        file.close()

    def get_current_date_time_string(self):
        currentDateTime = datetime.now()
        return currentDateTime.strftime("%d-%m-%y_%H-%M")
