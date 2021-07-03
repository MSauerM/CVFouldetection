import cv2 as cv

import appconfig
from BasicFramework.Frame import Frame


class VideoPreProcessor:

    frame_list = []
    filepath = None

    def __init__(self, filename: str):
        print("Initialize VideoPreProcessor")
        # load file at the file name
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

            preproc_frame = Frame(pixels=frame, timestamp=timestamp, framecount= frameIndex)
            self.frame_list.append(preproc_frame)

        print("Framecount: {count}".format(count=len(self.frame_list)))
        capture.release()
        #cv.destroyAllWindows()