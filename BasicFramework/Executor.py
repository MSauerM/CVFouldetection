import appconfig
from BasicFramework.FileWriter import FileWriter
from BasicFramework.VideoPreProcessor import VideoPreProcessor
from Fouldetection.FoulDetector import FoulDetector
from Fouldetection.FoulDetectorThread import FoulDetectorThread
from InputGUI.VideoPlayer import VideoPlayer
import os.path
import time
from CVUtility.PerformanceTimer import PerformanceTimer


class Executor:
    """
    A class for starting the execution of implemented modules
    .........

    Attributes:
    --------------
    timer : PerformanceTimer
        measuring the time spent for the whole processing
    preProcessor : VideoPreProcessor
        container for processing the loaded video material
    foulDetector : FoulDetector
        process the input video to gain information about fouls

    Methods:
    --------------
    execute(options)
        Starts the execution of all connected modules
    interrupt()
        Interrupts processing
    """
    def __init__(self):
        self.timer = PerformanceTimer()
        self.preProcessor = None

    def execute(self, options: dict):
        self.timer.start()
        self.preProcessor = VideoPreProcessor(options["video_fname"])

        if options["fouldetector"] is not None:
            if appconfig.use_multithreading is True:
                foulDetectorThread = FoulDetectorThread(options["video_fname"], False)
                foulDetectorThread.start()
            else:
                self.foulDetector = FoulDetector(self.preProcessor)
                self.foulDetector.process()

                if options["fouldetector"]["create_video"] is True:
                    if options["fouldetector"].get("video_output_name") is not None:
                        filename = self.foulDetector.createVideo(options["fouldetector"]["video_output_name"])
                    else:
                        filename = self.foulDetector.createVideo()
                    if options["fouldetector"]["show_video"] is True:
                        while not os.path.exists(filename):
                            time.sleep(1)
                        if os.path.isfile(filename):
                            print("Load Video")
                            videoPlayer = VideoPlayer()
                            videoPlayer.loadFile(filename)
                        else:
                            raise ValueError("No file at " % filename)

        self.timer.end()
        if options["fouldetector"] is not None:
            self.foulDetector.overall_time = self.timer.get_time()
            if options["fouldetector"].get("text_output_name") is not None:
                fileWriter = FileWriter(options["fouldetector"]["text_output_name"])
            else:
                fileWriter = FileWriter("Fouldetector_txt_out")
            fileWriter.set_output_directory("./output_info/")
            fileWriter.write_file(self.foulDetector)

    def interrupt(self):
        if self.foulDetector is not None:
            self.foulDetector.interruptProcessing()
