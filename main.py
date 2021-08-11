from PyQt5.QtCore import QCoreApplication

from BasicFramework.Executor import Executor
from BasicFramework.VideoPreProcessor import VideoPreProcessor
from Fouldetection.FoulDetectorThread import FoulDetectorThread
from InputGUI.GUIMain import start_GUI
import struct
import argparse
import sys

parser = argparse.ArgumentParser(description="Choose which clip should be processed")
parser.add_argument('-f', '--filename', type=str, metavar='', required=False, help='Name of the processed file')
parser.add_argument('-v', '--video', type=str, metavar='', required=False, help='Name of the video, which will be created as output' )

args = parser.parse_args()

if __name__ == '__main__':
    print("Start dialog")
    print (struct.calcsize("P")*8)
    if len(sys.argv) > 1:
        print('Console Execution')
        options = dict()
        options["video_preprocessor"] = VideoPreProcessor(args.filename)
        options["video_fname"] = args.filename
        options["fouldetector"] = dict()
        if args.video is not None:
            options["fouldetector"]["create_video"] = True
        else:
            options["fouldetector"]["create_video"] = False
        #options["fouldetector"]["show_video"] = self.shouldShowVideo
        executor = Executor()
        executor.execute(options)
        #app = QCoreApplication([])
        #thread = FoulDetectorThread(args.filename, args.video)
        #thread.finished.connect(app.exit)
        #thread.start()
        #sys.exit(app.exec_())  # Konsolensteuerung funktioniert derzeit nicht mit Executor
        #preProcessor = VideoPreProcessor(args.filename)
        #foulDetector = FoulDetector(preProcessor)
        #foulDetector.process()
        #foulDetector.createVideo(args.video)
    else:
        start_GUI()