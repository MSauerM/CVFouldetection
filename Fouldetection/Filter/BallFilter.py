import numpy as np

from Fouldetection.Filter import Filter
from cv2 import cv2 as cv

class BallFilter(Filter):

    def __init__(self):
        super().__init__()

    def filter(self, frame):

        frame_hsv = cv.cvtColor(frame.getPixels(), cv.COLOR_BGR2HSV)
        # weißFilter
        lower_white = np.array([60, 0, 120])
        upper_white = np.array([130, 25, 255])

        whiteFiltered = cv.inRange( frame_hsv, lower_white, upper_white)

        cv.imshow("white filtered", whiteFiltered)
        cv.waitKey(0)

        gray_frame = cv.cvtColor(frame.getPixels(), cv.COLOR_BGR2GRAY)
        #cv.imshow("Gray_Frame", gray_frame)
        #cv.waitKey(0)

        #circles = cv.HoughCircles(gray_frame, cv.HOUGH_GRADIENT, 1, 1)
        #if circles is not None:
        #    circles = np.uint16(np.around(circles))
        #    for circle in circles[0, :]:
        #        center = (circle[0], circle[1])
        #        cv.circle(frame.getPixels(), center, 1, (0, 100, 100), 3)
        #        radius = circle[2]
       #         cv.circle(frame.getPixels(), center, radius, (255, 0, 255), 3)

        cv.imshow("Detected Circles", frame.getPixels())
        cv.waitKey(0)
