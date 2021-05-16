import math

from BasicFramework.Frame import Frame

from Fouldetection.Filter.Filter import Filter
from cv2 import cv2 as cv
import numpy as np
import CVUtility.ImageUtility as utility

class GrassFilter(Filter):

    def __init__(self):
        super().__init__()

    def filter(self, frame: Frame):
        #print("This is a grass filter for filtering the court of of the picture")
        # option 1 (simple): filter green color

        blurred_image = cv.GaussianBlur(frame.getPixels(), (5,5), 0)
        utility.showResizedImage("Blurred Image", blurred_image, 0.4)

        frame_hsv = cv.cvtColor(blurred_image, cv.COLOR_BGR2HSV)
        lower_green = np.array([30, 40, 40])
        upper_green = np.array([90, 255, 255])

        #dst = cv.Canny(frame.getPixels(), 50, 200, None, 3)

        #cv.imshow("Dst", dst)

        #lines = cv.HoughLines(dst, 1 , np.pi/ 180, 150, None, 0, 0) # cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10) #
        #if lines is not None:
        #    for i in range(0, len(lines)):
       #         rho = lines[i][0][0]
        #        theta = lines[i][0][1]
       #         a = math.cos(theta)
       #         b = math.sin(theta)
       #         x0 = a * rho
       #         y0 = b * rho
       #         pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
       #         pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
       #         cv.line(frame.getPixels(), pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)

        #cv.imshow("Lines", frame.getPixels())
        utility.showResizedImage("Lines", frame.getPixels(), 0.4)

        mask = cv.inRange(frame_hsv, lower_green, upper_green)
#        cv.imshow("mask", mask)
        utility.showResizedImage("Mask", mask, 0.4)

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
        combined = cv.dilate(combined, kernel, iterations=1)#cv.morphologyEx(combined, cv.MORPH_CLOSE, kernel= kernel,iterations=5)
       # cv.imshow("Res", res)
       # cv.imshow("White Mask", white_mask)
       # cv.imshow("White Mask Inverted", white_mask_inv)
        utility.showResizedImage("CVFouldetection GrassFilter", combined, 0.4)

        green_mask = cv.erode(mask, kernel, iterations=5)

        green_mask = cv.morphologyEx(green_mask, cv.MORPH_CLOSE, kernel= kernel, iterations=5)
        utility.showResizedImage("GrassFilter - Opened Green Mask", green_mask, 0.4)

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
            cv.drawContours(drawing, contours, i, (0, 255, 0))
            cv.drawContours(drawing, hull_list, i, (0, 0, 255))
            hullArea =cv.contourArea(hull_list[i])
            if greatestArea < hullArea:
                greatestArea = hullArea
                greatestAreaIndex = i

        fieldAreaDrawing = np.zeros((blurred_image.shape[0], blurred_image.shape[1], 3), dtype=np.uint8)
        cv.fillPoly(fieldAreaDrawing, [hull_list[greatestAreaIndex]], (255, 255, 255))
        utility.showResizedImage("GrassFilter - Opened Drawing - Contours", drawing, 0.4)
        utility.showResizedImage("GrassFilter - Field Area", fieldAreaDrawing, 0.4)
        #convert fieldAreaDrwa
        field = cv.bitwise_and(res, fieldAreaDrawing)
        utility.showResizedImage("GrassFilter - Field", field, 0.4)

        #        cv.imshow("CVFouldetection GrassFilter", combined)
        #   cv.waitKey(0)
       # return thresh
        return combined

        # option 2 (complex): do it as the paper says