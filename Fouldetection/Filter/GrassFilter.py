import math

from BasicFramework.Frame import Frame

from Fouldetection.Filter.Filter import Filter
from cv2 import cv2 as cv
import numpy as np
import CVUtility.ImageUtility as utility


class GrassFilter(Filter):
    """
        Class for filtering the pitch of the frames
        ......

        Attributes
        -----------------

        Methods
        -----------------
            filter(frame, preprocessed_frames)
                processes the frame and returns a grass filtered image and
                a mask of the region of interest
        """
    def __init__(self):
        super().__init__()

    def filter(self, frame: Frame, preprocessed_frames=None):

        blurred_image = cv.GaussianBlur(frame.get_pixels(), (5, 5), 0)
        utility.showResizedImage("Blurred Image", blurred_image, 0.4)

        frame_hsv = cv.cvtColor(blurred_image, cv.COLOR_BGR2HSV)
        lower_green = np.array([30, 40, 40])
        upper_green = np.array([90, 255, 255])

        utility.showResizedImage("Lines", frame.get_pixels(), 0.4)

        mask = cv.inRange(frame_hsv, lower_green, upper_green)
        utility.showResizedImage("Mask", mask, 0.4)

        res = cv.bitwise_and(frame.get_pixels(), frame.get_pixels(), mask=mask)
        res_bgr = cv.cvtColor(res, cv.COLOR_HSV2BGR)
        res_gray = cv.cvtColor(res_bgr, cv.COLOR_BGR2GRAY)

        kernel = np.ones((13, 13), np.uint8)
        thresh = cv.threshold(res_gray, 110, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU) [1]
        thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

        lower_white = np.array([0, 0, 130])
        upper_white = np.array([255, 255, 255])

        white_mask = cv.inRange(res, lower_white, upper_white)
        kernel = np.ones((5, 5), np.uint8)

        white_mask = cv.dilate(white_mask, kernel, iterations=2)

        white_mask_inv = cv.bitwise_not(white_mask)
        combined = cv.bitwise_and(thresh, white_mask_inv, mask=white_mask_inv)
        combined = cv.dilate(combined, kernel, iterations=1)

        green_mask = cv.erode(mask, kernel, iterations=15)
        utility.showResizedImage("GrassFilter - Eroded", green_mask, 0.4)
        green_mask = cv.morphologyEx(green_mask, cv.MORPH_CLOSE, kernel= kernel, iterations=5)

        contours, _ = cv.findContours(green_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        green_mask_copy = green_mask
        hull_list = []
        for i in range(len(contours)):
            hull = cv.convexHull(contours[i])
            hull_list.append(hull)

        drawing = np.zeros((blurred_image.shape[0], blurred_image.shape[1], 3), dtype=np.uint8)
        greatestArea = 0
        greatestAreaIndex = -1
        for i in range(len(contours)):
            cv.drawContours(drawing, contours, i, (0, 255, 0), 2)
            cv.drawContours(drawing, hull_list, i, (0, 0, 255), 2)
            hullArea =cv.contourArea(hull_list[i])
            if greatestArea < hullArea:
                greatestArea = hullArea
                greatestAreaIndex = i

        fieldAreaDrawing = np.zeros((blurred_image.shape[0], blurred_image.shape[1], 3), dtype=np.uint8)
        cv.fillPoly(fieldAreaDrawing, [hull_list[greatestAreaIndex]], (255, 255, 255))
        utility.showResizedImage("GrassFilter - Opened Drawing - Contours", drawing, 0.4)
        utility.showResizedImage("GrassFilter - Field Area", fieldAreaDrawing, 0.4)
        #convert fieldAreaDrwa
        field = cv.bitwise_and(frame.get_pixels(), fieldAreaDrawing)
        utility.showResizedImage("GrassFilter - Field", field, 0.4)
        fieldAreaDrawing = cv.cvtColor(fieldAreaDrawing, cv.COLOR_BGR2GRAY)
        combined = cv.bitwise_and(combined, fieldAreaDrawing)
        utility.showResizedImage("GrassFilter - Combined Final", combined, 0.4)

        return (combined, fieldAreaDrawing)
