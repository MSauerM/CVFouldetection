import appconfig
from BasicFramework.VideoPreProcessor import VideoPreProcessor
from Fouldetection.FoulDetector import FoulDetector
from Fouldetection.FoulDetectorThread import FoulDetectorThread
from InputGUI.VideoPlayer import VideoPlayer


class Executor:

    def __init__(self):
        self.preProcessor = None

    def execute(self, options: dict):

        self.preProcessor = VideoPreProcessor(options["video_fname"])

        if options["fouldetector"] is not None:
            if appconfig.use_multithreading is True:
                foulDetectorThread = FoulDetectorThread(options["video_fname"], False)
                foulDetectorThread.start()
            else:
                self.foulDetector = FoulDetector(self.preProcessor)
                self.foulDetector.process()

                if options["fouldetector"]["create_video"] is True:
                    filename = self.foulDetector.createVideo()
                    if options["fouldetector"]["show_video"] is True:
                        videoPlayer = VideoPlayer()
                        videoPlayer.loadFile(filename)

    def interrupt(self):
        if self.foulDetector is not None:
            self.foulDetector.interruptProcessing()
