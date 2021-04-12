import cv2 as cv


class VideoPreProcessor:

    frame_list = []

    def __init__(self, filename: str):
        print("Initialize VideoPreProcessor")
        # load file at the file name
        capture = cv.VideoCapture(filename)
        self.frame_list = []
        # load video into single frames
        while capture.isOpened():
            ret, frame = capture.read()
            #cv.imshow("Frames", frame)
            #cv.waitKey(1)

            #convert frame to hsv
            #frame_hsv = cv.cvtColor(frame, cv.COLOR_RGB2HSV)

            if not ret:
                print("Ending Processing")
                break

            self.frame_list.append(frame)

        print("Framecount: {count}".format(count=len(self.frame_list)))
        capture.release()
        #cv.destroyAllWindows()