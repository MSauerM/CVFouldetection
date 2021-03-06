import os
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QFileDialog, QCheckBox, QRadioButton

from PyQt5.QtCore import QSize, Qt

import appconfig
from BasicFramework.VideoPreProcessor import VideoPreProcessor

import subprocess

from Fouldetection.FoulDetector import FoulDetector
from Fouldetection.FoulDetectorThread import FoulDetectorThread
from InputGUI.VideoPlayer import VideoPlayer
from cv2 import cv2 as cv

from BasicFramework.Executor import Executor


class VideoFileDialogWindow(QMainWindow):
    def __init__(self, app):
        global txts
        super().__init__()
        self.setMinimumSize(QSize(350, 200))
        self.setWindowTitle('Fouldetection - MP4 File Auswahl')

        self.shouldCreateVideo = False
        self.shouldShowVideo = False

        self.app = app
        self.executor = Executor()

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
            grid.addWidget(self.lbls[row], row, 2, 1, 3)

        selectButton = QPushButton('Auswählen')#'Select')
        selectButton.clicked.connect(self.select)
        grid.addWidget(selectButton, 5, 1, Qt.AlignRight)

        cancelButton = QPushButton('Abbrechen')
        cancelButton.clicked.connect(self.cancel)
        grid.addWidget(cancelButton, 5, 4, Qt.AlignRight)

        processButton = QPushButton('Verarbeiten')
        processButton.clicked.connect(lambda:self.processVideo(self.fileName))
        grid.addWidget(processButton, 5, 2, Qt.AlignRight)

        interruptProcessingButton = QPushButton('Unterbrechen')#'Interrupt')
        interruptProcessingButton.clicked.connect(lambda:self.interrupt())
        grid.addWidget(interruptProcessingButton, 5, 3, Qt.AlignRight)

        createVideoCheckbox = QCheckBox("Video erzeugen")#"Create Video")
        createVideoCheckbox.stateChanged.connect(self.createVideoCheckbox_Changed)
        grid.addWidget(createVideoCheckbox, 6, 2, Qt.AlignRight)

        showVideoCheckBox = QCheckBox("Erstelltes Video anzeigen" )#"Show Video after Processing")
        showVideoCheckBox.stateChanged.connect(self.showVideoCheckbox_Changed)
        #grid.addWidget(showVideoCheckBox, 6, 3, Qt.AlignRight)

        action_recognition_RadioButton = QRadioButton("Action Recognition")
        action_recognition_RadioButton.toggled.connect(lambda:self.processingType_State(action_recognition_RadioButton))
        action_recognition_RadioButton.setChecked(True)
        grid.addWidget(action_recognition_RadioButton, 6, 3, Qt.AlignRight)

        human_pose_estimation_RadioButton = QRadioButton("Human Pose Estimation")
        human_pose_estimation_RadioButton.setChecked(False)
        human_pose_estimation_RadioButton.toggled.connect(lambda: self.processingType_State(human_pose_estimation_RadioButton))
        grid.addWidget(human_pose_estimation_RadioButton, 6, 4, Qt.AlignRight)

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

    def processingType_State(self, b):
        if b.text() == "Action Recognition":
            if b.isChecked() == True:
                appconfig.use_action_recognition = True
                appconfig.use_human_pose_estimation = False
        if b.text() == "Human Pose Estimation":
            if b.isChecked() == True:
                appconfig.use_action_recognition = False
                appconfig.use_human_pose_estimation = True

    def processVideo(self, filename):
        options = dict()
        options["video_preprocessor"] = VideoPreProcessor(filename)
        options["video_fname"] = filename
        options["fouldetector"] = dict()
        options["fouldetector"]["create_video"] = self.shouldCreateVideo
        options["fouldetector"]["show_video"] = self.shouldShowVideo

        self.executor.execute(options)

    def interrupt(self):
        self.executor.interrupt()
