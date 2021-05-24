import cv2 as cv
import numpy as np

from Fouldetection.ColorHistogram import ColorHistogram
from CVUtility import ImageUtility as utility

class TeamColorCalibration:

    isCalibrated = False
    colors_list = []

    def __init__(self):
        print ("TeamColorCalibration")

    def calibrate(self, img, mask):
        print ("Calibrate")
        histogram = ColorHistogram(img, mask)
        # eventuell noch ein Opening laufen lassen?()
        # höchste Hue Peaks ausgeben lassen


        # 1
        histogram_colors = histogram.get_main_colors(5)
        histogram.show_histogram()
        first_color = histogram_colors[0]
        second_color = histogram_colors[1]

        self.colors_list.append(first_color)
        self.colors_list.append(second_color)

        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        image_one = cv.inRange(img_hsv, np.array([first_color[0]-20, 100, 100]), np.array([first_color[0]+20, 255, 255]))
        image_two = cv.inRange(img_hsv, np.array([second_color[0]-20, 100, 100]), np.array([second_color[0]+20, 255, 255]))

        utility.showResizedImage("TeamColorCalibration - Image One ", image_one, 0.4)
        utility.showResizedImage("TeamColorCalibration - Image Two ", image_two, 0.4)

        utility.showResizedImage("TeamColorCalibration - Image", img, 0.4)
        utility.showResizedImage("TeamColorCalibration - Mask", mask, 0.4)
        utility.showResizedImage("TeamColorCalibration - Fusion", cv.bitwise_and(img, img, mask= mask), 0.4)
        self.isCalibrated = True
