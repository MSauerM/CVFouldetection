import os
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QFileDialog, QCheckBox

from PyQt5.QtCore import QSize, Qt

from BasicFramework.VideoPreProcessor import VideoPreProcessor

import subprocess

from Fouldetection.FoulDetector import FoulDetector
from InputGUI.VideoPlayer import VideoPlayer


class VideoFileDialogWindow(QMainWindow):
    def __init__(self, app):
        global txts
        super().__init__()
        self.setMinimumSize(QSize(350, 200))
        self.setWindowTitle('Fouldetection - MP4 File Auswahl')

        self.shouldCreateVideo = False
        self.shouldShowVideo = False

        self.app = app

        wid = QWidget()
        self.setCentralWidget(wid)
        grid = QGridLayout()
        wid.setLayout(grid)

        self.lbls = []

        row = 0
        for s in ['Filename:', 'Größe:', 'Länge:']:
            grid.addWidget(QLabel(s), row, 1)
            row += 1

        for row in range(3):
            self.lbls += [QLabel('---')]
            grid.addWidget(self.lbls[row], row, 2)

        selectButton = QPushButton('Select')
        selectButton.clicked.connect(self.select)
        grid.addWidget(selectButton, 5, 1, Qt.AlignRight)

        cancelButton = QPushButton('Abbrechen')
        cancelButton.clicked.connect(self.cancel)
        grid.addWidget(cancelButton, 5, 3, Qt.AlignRight)

        processButton = QPushButton('Verarbeiten')
        processButton.clicked.connect(lambda:self.processVideo(self.fileName))
        grid.addWidget(processButton, 5, 2, Qt.AlignRight)

        createVideoCheckbox = QCheckBox("Create Video")
        createVideoCheckbox.stateChanged.connect(self.createVideoCheckbox_Changed)
        grid.addWidget(createVideoCheckbox, 6, 2, Qt.AlignRight)

        showVideoCheckBox = QCheckBox("Show Video after Processing")
        showVideoCheckBox.stateChanged.connect(self.showVideoCheckbox_Changed)
        grid.addWidget(showVideoCheckBox, 6, 3, Qt.AlignRight)

    def select(self):
        filter = "mp4(*.mp4)"
        (fname, _) = QFileDialog.getOpenFileName(self, filter= filter)
        if fname != '':
            self.fileName = fname
            self.lbls[0].setText(fname)
            try:
                size = os.path.getsize(fname)

                self.lbls[1].setText("{size}".format(size=size))
                self.lbls[2].setText("{length}".format(length= self.getVideoLength(fname)))
            except BaseException as ex:
                print('Fehler', ex)

    def cancel(self):
        self.app.quit()

    def getVideoLength(self, fname):
       # https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", fname],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        return float(result.stdout)

    def createVideoCheckbox_Changed(self, state):
        self.shouldCreateVideo = (state == Qt.Checked)

    def showVideoCheckbox_Changed(self, state):
        self.shouldShowVideo = (state == Qt.Checked)


    def processVideo(self, filename):
        self.preProcessor = VideoPreProcessor(filename)
        self.foulDetector = FoulDetector(self.preProcessor)
        self.foulDetector.process()

        if self.shouldCreateVideo:
            filename = self.foulDetector.createVideo()
            if self.shouldShowVideo:
                videoPlayer = VideoPlayer()
                videoPlayer.loadFile(filename)

