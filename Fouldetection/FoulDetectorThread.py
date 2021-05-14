from PyQt5.QtCore import QThread

from Fouldetection.FoulDetector import FoulDetector


class FoulDetectorThread(QThread):

    def __init__(self, filename: str, createVideo: bool):
        super(QThread, self).__init__()
        self._filename = filename
        self._createVideo = createVideo


    def run(self) -> None:
        foulDetector = FoulDetector(filename=self._filename)
        foulDetector.process()
        if self._createVideo:
            foulDetector.createVideo()
