from BasicFramework.VideoPreProcessor import VideoPreProcessor
from Fouldetection.FoulDetector import FoulDetector
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
        preProcessor = VideoPreProcessor(args.filename)
        foulDetector = FoulDetector(preProcessor)
        foulDetector.process()
        foulDetector.createVideo(args.video)
    else:
        start_GUI()