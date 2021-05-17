import numpy as np

from cv2 import cv2 as cv

from BasicFramework.Frame import Frame
from Fouldetection.Filter.Filter import Filter
from CVUtility import ImageUtility as utility


class BallFilter(Filter):

    previous_ball_positions = []

    def __init__(self):
        super().__init__()

    def filter(self, frame: Frame, preprocessed_frames=None):
        img = frame.getPixels()
        img_hsv = cv.cvtColor(frame.getPixels(), cv.COLOR_BGR2HSV)
        # weißFilter
        lower_white = np.array([0, 0, 160])# np.array([60, 0, 120])
        upper_white = np.array([255, 255, 255])# np.array([130, 25, 255])

        whiteFiltered = cv.inRange( img_hsv, lower_white, upper_white)

        kernel = np.ones( (5,5), np.uint8)

#        whiteFiltered = cv.erode(whiteFiltered, kernel, iterations=5)
        whiteFiltered = cv.morphologyEx(whiteFiltered, cv.MORPH_CLOSE, kernel)
        whiteFiltered = cv.bitwise_and(whiteFiltered, preprocessed_frames[1])
        utility.showResizedImage("Ball Filter - White Filtered", whiteFiltered, 0.4)

        gray_img = cv.cvtColor(frame.getPixels(), cv.COLOR_BGR2GRAY)
        thresh = cv.threshold(gray_img, 150, 255, cv.THRESH_OTSU)[1]
        utility.showResizedImage("Ball Filter - Thresh", thresh, 0.4)

        ballCandidates = []

        circles = cv.HoughCircles(whiteFiltered, cv.HOUGH_GRADIENT, 1, 20)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0, :]:
                center = (circle[0], circle[1])
                cv.circle(img, center, 1, (0, 100, 100), 3)
                radius = circle[2]
                cv.circle(img, center, radius, (255, 0, 255), 3)

        utility.showResizedImage("Detected Circles", img, 0.4)

        (contours, hierarchy) = cv.findContours(whiteFiltered, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x, y, w, h = cv.boundingRect(c)
            if( (w < 40 and h < 40) and (w > 20 and h>20)):
                cv.rectangle(img, (x,y), (x+w,y+h), (255,0,255), 3)
            #cv.drawContours(img, contours, -1, (0,0, 255), 3)

        utility.showResizedImage("Ball Candidates", img, 0.4)

        return ballCandidates