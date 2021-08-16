from PyQt5.QtCore import QCoreApplication

import appconfig
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
parser.add_argument('-o', '--output', type=str, metavar='', required=False, help='Name of the output text file')
parser.add_argument('--action_recognition', type=bool, required=False, default=False)
parser.add_argument('--human_pose_estimation', type=bool, required=False, default=False)

args = parser.parse_args()

if __name__ == '__main__':
    print("Start dialog")
    print (struct.calcsize("P")*8)
    if len(sys.argv) > 1:
        print('Console Execution')
        options = dict()
        #options["video_preprocessor"] = VideoPreProcessor(args.filename)
        options["video_fname"] = args.filename
        options["fouldetector"] = dict()
        if args.video is not None:
            options["fouldetector"]["create_video"] = True
            options["fouldetector"]["video_output_name"] = args.video
        else:
            options["fouldetector"]["create_video"] = False
        if args.output is not None:
            options["fouldetector"]["text_output_name"] = args.output
        if args.action_recognition is not None:
            options["fouldetector"]["action_recognition"] = args.action_recognition
        options["fouldetector"]["show_video"] = False
        appconfig.use_action_recognition = args.action_recognition
        appconfig.use_human_pose_estimation = args.human_pose_estimation

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