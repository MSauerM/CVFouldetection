import cv2 as cv

import appconfig
from BasicFramework.Frame import Frame
from CVUtility.PerformanceTimer import PerformanceTimer


class VideoPreProcessor:
    """
        Class for ....
        ......

        Attributes
        -----------------



        Methods
        -----------------

        """
    frame_list = []
    filepath = None

    def __init__(self, filename: str):
        print("Initialize VideoPreProcessor")
        self.preprocess(filename)

    def preprocess(self, filename:str):
        self.timer = PerformanceTimer()
        self.timer.start()
        # load file with the file name
        self.filepath = filename
        capture = cv.VideoCapture(filename)
        self.frame_list = []
        # load video into single frames
        while capture.isOpened():
            frameIndex = int(capture.get(cv.CAP_PROP_POS_FRAMES))
            timestamp = capture.get(cv.CAP_PROP_POS_MSEC)
            ret, frame = capture.read()

            if not ret or appconfig.max_frame_amount < frameIndex:
                print("Ending Processing")
                break

            preproc_frame = Frame(pixels=frame, timestamp=timestamp, frameindex=frameIndex)
            self.frame_list.append(preproc_frame)

        print("Framecount: {count}".format(count=len(self.frame_list)))
        capture.release()
        self.timer.end()
