import numpy as np

from BasicFramework.Frame import Frame
from CVUtility.BoundingBoxInformation import BoundingBoxInformation

import cv2 as cv
import CVUtility.ImageUtility as utility
from Fouldetection.Filter.Filter import Filter


class PlayerFilter(Filter):

    def __init__(self):
        super().__init__()

    def filter(self, frame: Frame, preprocessed_frames = None):
        # canny Edge detection
        img = frame.getPixels()
        frame_hsv = cv.cvtColor(frame.getPixels(), cv.COLOR_BGR2HSV)
        #frame_thresh = cv.cvtColor(preprocessed_frames, cv.Color_gray2)
        #edges = cv.Canny(frame_hsv, 100, 200)

        kernel = np.ones( (5,5), np.uint8)

        preprocessed_frames = cv.dilate(preprocessed_frames, kernel, iterations=3)

        (contours, hierarchy) = cv.findContours(preprocessed_frames, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


        player_img = cv.bitwise_and(frame.getPixels(), frame.getPixels(), mask=preprocessed_frames)
        edges = cv.Canny(img, 50, 150)
        # Hough Lines on this edge detector?
        utility.showResizedImage("Player Filter - Edges", edges, 0.4)

        boundingBoxInformation_list = []

       # cv.imshow("player Image", player_img)
       # cv.waitKey(0)
        #utility.showResizedImage("Player Image", player_img, 0.4)
        font = cv.FONT_HERSHEY_PLAIN

        for c in contours:
            x, y, w, h = cv.boundingRect(c)
            if ( (w > 15 and h > 20)  and (w < 450 and h < 450)):
                #cv.drawContours(frame, cv.boundingRect(c), -1, (255, 0, 0),3)
                boundingBoxInformation_list.append(BoundingBoxInformation(frame.getFrameCount(), x, y, w, h))
                cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
                cv.putText(img, "{w}/ {h}".format(w= w, h=h), (x-2, y-2), font, 0.8, (0, 255, 0), 2, cv.LINE_AA)
        cv.drawContours(img, contours, -1, (0, 0, 255), 3)
        utility.showResizedImage("Player Filter - Result", img, 0.4)
        #cv.imshow("Edges", edges)
        #cv.imshow("Output", frame.getPixels())
        #cv.waitKey(0)
        #utility.showResizedImage("Edges", edges, 0.4)
        #utility.showResizedImage("Output", frame.getPixels(), 0.4)
        return boundingBoxInformation_list