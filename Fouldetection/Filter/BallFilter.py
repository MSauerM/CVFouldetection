import numpy as np

from cv2 import cv2 as cv

from BasicFramework.Frame import Frame
from Fouldetection.Filter.Filter import Filter
from CVUtility import ImageUtility as utility

class BallFilter(Filter):

    def __init__(self):
        super().__init__()

    def filter(self, frame: Frame, preprocessed_frames=None):
        img = frame.getPixels()
        img_hsv = cv.cvtColor(frame.getPixels(), cv.COLOR_BGR2HSV)
        # weißFilter
        lower_white = np.array([0, 0, 160])# np.array([60, 0, 120])
        upper_white = np.array([255, 255, 255])# np.array([130, 25, 255])

        whiteFiltered = cv.inRange( img_hsv, lower_white, upper_white)

        utility.showResizedImage("White Filtered", whiteFiltered, 0.4)
        #cv.imshow("white filtered", whiteFiltered)
        #cv.waitKey(0)

        gray_img = cv.cvtColor(frame.getPixels(), cv.COLOR_BGR2GRAY)
        #cv.imshow("Gray_Frame", gray_frame)
        #cv.waitKey(0)

        circles = cv.HoughCircles(whiteFiltered, cv.HOUGH_GRADIENT, 1, 20)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0, :]:
                center = (circle[0], circle[1])
                cv.circle(img, center, 1, (0, 100, 100), 3)
                radius = circle[2]
                cv.circle(img, center, radius, (255, 0, 255), 3)

        utility.showResizedImage("Detected Circles", img, 0.4)
        #cv.imshow("Detected Circles", img)
        #cv.waitKey(0)
