import cv2
import numpy as np

from cv2 import cv2 as cv

from BasicFramework.Frame import Frame
from Fouldetection.Filter.Filter import Filter
from CVUtility import ImageUtility as utility
from CVUtility.PerformanceTimer import PerformanceTimer

class BallFilter(Filter):

    previous_ball_positions = []

    def __init__(self):
        super().__init__()
        self._timer = PerformanceTimer("Ball Filter")

    def filter(self, frame: Frame, preprocessed_frames=None):
        img = frame.get_pixels()
        img_hsv = cv.cvtColor(frame.get_pixels(), cv.COLOR_BGR2HSV)
        # weißFilter
        lower_white = np.array([0, 0, 160])# np.array([60, 0, 120])
        upper_white = np.array([255, 255, 255])# np.array([130, 25, 255])

        whiteFiltered = cv.inRange( img_hsv, lower_white, upper_white)

        kernel = np.ones( (5,5), np.uint8)

        grassFilteredMask = preprocessed_frames[0]

#        whiteFiltered = cv.erode(whiteFiltered, kernel, iterations=5)
        whiteFiltered = cv.morphologyEx(whiteFiltered, cv.MORPH_CLOSE, kernel, iterations=5)
        grassFilteredMask = cv.morphologyEx(grassFilteredMask, cv.MORPH_CLOSE, kernel, iterations=5)
        whiteFiltered = cv.bitwise_and(whiteFiltered, preprocessed_frames[1])
        #utility.showResizedImage("Ball Filter - White Filtered", whiteFiltered, 0.4)


        gray_img = cv.cvtColor(frame.get_pixels(), cv.COLOR_BGR2GRAY)
        thresh = cv.threshold(gray_img, 150, 255, cv.THRESH_BINARY)[1]
        thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

        img = cv.GaussianBlur(img,(5,5),0)
      #  img = cv.bitwise_and(img, img, mask=preprocessed_frames[0])
        edge = cv.Canny(img, 50, 150)
        edge = cv.bitwise_and(edge, preprocessed_frames[1])


        closed_edges = cv.morphologyEx(edge, cv.MORPH_CLOSE, kernel, iterations=3)
       # closed_edges = cv.morphologyEx(closed_edges, cv.MORPH_OPEN, kernel, iterations=2)
       # closed_edges = cv.subtract(closed_edges, preprocessed_frames[0])
        utility.showResizedImage("Ball Filter - Closed Edges", closed_edges, 0.4)
        utility.showResizedImage("Ball Filter - gras Filtered Frame", preprocessed_frames[0], 0.4)

        #utility.showResizedImage("Ball Filter - Thresh", thresh, 0.4)
        #utility.showResizedImage("Ball Filter - GrassFiltered", grassFilteredMask, 0.4)


        #circles = cv.HoughCircles(closed_edges, cv.HOUGH_GRADIENT, 1.2, 50)
        #if circles is not None:
        #    circles = np.uint16(np.around(circles))
       #     for circle in circles[0, :]:
       #         center = (circle[0], circle[1])
       #         cv.circle(img, center, 1, (0, 100, 100), 3)
        #        radius = circle[2]
       #         cv.circle(img, center, radius, (255, 0, 255), 3)

        #utility.showResizedImage("Detected Circles", img, 0.4)

        ballCandidates = []

        self._timer.start()
        (contours, hierarchy) = cv.findContours(closed_edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for c in contours:
            circle = cv.minEnclosingCircle(c)
            circleCenter = (int(circle[0][0]), int(circle[0][1]))
            circleRadius = int(circle[1])

            rect = cv.minAreaRect(c)
            box = cv.boxPoints(rect)
            box = np.intp(box)
            if 5 < circleRadius < 20:
                x, y, w, h = cv2.boundingRect(box)
                crop = closed_edges[y:y+h, x:x+w]
                widthHeightRatio = w/h
                #black_pixels = (w*h)
                white_pixel_amount = cv.countNonZero(crop) #/ (black_pixels +1)
                # ball Candidate
                # widthHeightRatio has to be near to one plus high white to dark pixel Ratio
                ballCandidates.append([(circleCenter, circleRadius), white_pixel_amount, widthHeightRatio])
                #utility.showResizedImage("Crop ", crop, 1)
                cv.circle(img, circleCenter, circleRadius, (0, 255, 255), 3)
                cv.drawContours(img, [box], 0, (255, 0, 255), 3)
            #x, y, w, h = cv.boundingRect(c)
            #if( (w < 40 and h < 40) and (w > 20 and h>20)):
             #   cv.rectangle(img, (x,y), (x+w,y+h), (255,0,255), 3)
            #cv.drawContours(img, contours, -1, (0,0, 255), 3)

        # remove all candidates from ballCandidates which have not at least a certain amount of white pixels in edge
        # and remove candidates which have to much
        ballCandidates = [x for x in ballCandidates if x[1] > 150]
        #print(ballCandidates)

        # remove all candidates from ballCandidates which is not in the range of the intervall regarding width height ratio
        ballCandidates = [x for x in ballCandidates if 0.25 < x[2] < 1.75]
        self._timer.end()
        #print(self._timer)
        #self._timer.end()
        #print(self._timer) on Average 0.3
        ###################################### Not the bottle neck
        #self._timer.start()
        for candidate in ballCandidates:
            cv.putText(img,
                       "{w}/ {h}".format(w=candidate[0][0][0], h=candidate[0][0][1]),
                       (candidate[0][0][0] - 2, candidate[0][0][1] - 2),
                       cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv.LINE_4)
            cv.circle(img, candidate[0][0], candidate[0][1], (0, 255, 255), 3)
        #self._timer.end()
        #print(self._timer)
        ######################################

        utility.showResizedImage("Ball Candidates", img, 0.4)

        return ballCandidates