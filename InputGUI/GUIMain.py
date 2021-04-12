#from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QApplication, QLabel
from InputGUI.VideoFileDialogWindow import VideoFileDialogWindow

def start_GUI():
    print("startGui")
    app = QApplication([])
    videoFileDialogWindow = VideoFileDialogWindow(app)
    videoFileDialogWindow.show()
    app.exec_()