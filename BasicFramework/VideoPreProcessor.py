import cv2 as cv

from BasicFramework.Frame import Frame


class VideoPreProcessor:

    frame_list = []

    def __init__(self, filename: str):
        print("Initialize VideoPreProcessor")
        # load file at the file name
        capture = cv.VideoCapture(filename)
        self.frame_list = []
        # load video into single frames
        while capture.isOpened():
            frameIndex = capture.get(cv.CAP_PROP_POS_FRAMES)
            timestamp = capture.get(cv.CAP_PROP_POS_MSEC)
            ret, frame = capture.read()

            if not ret:
                print("Ending Processing")
                break

            preproc_frame = Frame(pixels=frame, timestamp=timestamp, framecount= frameIndex)
            self.frame_list.append(preproc_frame)

        print("Framecount: {count}".format(count=len(self.frame_list)))
        capture.release()
        #cv.destroyAllWindows()