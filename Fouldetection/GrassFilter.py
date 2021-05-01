from BasicFramework.Frame import Frame
from Fouldetection.Filter import Filter
from cv2 import cv2 as cv
import numpy as np


class GrassFilter(Filter):

    def __init__(self):
        super().__init__()

    def filter(self, frame: Frame):
        #print("This is a grass filter for filtering the court of of the picture")
        # option 1 (simple): filter green color

        frame_hsv = cv.cvtColor(frame.getPixels(), cv.COLOR_BGR2HSV)
        lower_green = np.array([36, 40, 40])
        upper_green = np.array([86, 255, 255])


        mask = cv.inRange(frame_hsv, lower_green, upper_green)
        cv.imshow("mask", mask)

        res = cv.bitwise_and(frame.getPixels(), frame.getPixels(), mask=mask)
        res_bgr = cv.cvtColor(res, cv.COLOR_HSV2BGR)
        res_gray = cv.cvtColor(res_bgr, cv.COLOR_BGR2GRAY)

        kernel = np.ones((13, 13), np.uint8)
        thresh = cv.threshold(res_gray, 110, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU) [1]
        thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

        lower_white = np.array([0, 0, 130])
        upper_white = np.array([255, 255, 255])

        white_mask = cv.inRange(res, lower_white, upper_white)
        #white_mask = cv.inRange(frame_hsv, lower_white, upper_white)
        kernel = np.ones((5, 5), np.uint8)

        white_mask = cv.dilate(white_mask, kernel, iterations=2)

        #white_mask_xor = cv.bitwise_xor()
        white_mask_inv = cv.bitwise_not(white_mask)
        combined = cv.bitwise_and(thresh, white_mask_inv, mask=white_mask_inv)#cv.bitwise_not(thresh, mask=white_mask)

       # cv.imshow("Res", res)
       # cv.imshow("White Mask", white_mask)
       # cv.imshow("White Mask Inverted", white_mask_inv)
        cv.imshow("CVFouldetection GrassFilter", combined)
        cv.waitKey(0)
       # return thresh
        return combined

        # option 2 (complex): do it as the paper says