import cv2 as cv
import numpy as np

import appconfig
from Fouldetection.DataStructures.ColorHistogram import ColorHistogram
from CVUtility import ImageUtility as utility

class TeamColorCalibration:

    isCalibrated = False
    colors_list = []

    isBuli = True

    def __init__(self):
        print ("TeamColorCalibration")

    def calibrate(self, img, mask):
        print ("Calibrate")
        logo_poly = np.array([[[90,95], [90,45], [460,45], [460, 95]]])
        mask = cv.fillPoly(mask, logo_poly, 0)

        histogram = ColorHistogram(img, mask)

        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        if self.isBuli:
            color_point_1 = [1225, 75]
            color_point_2 = [1715,  75]
            color_1 = img_hsv[color_point_1[1], color_point_1[0]][0]
            color_2 = img_hsv[color_point_2[1], color_point_2[0]][0]
        utility.showResizedImage("TeamColorCalibration - Fusion", cv.bitwise_and(img, img, mask= mask), 0.4)

        self.team_color_orientation = {'blue': 120, 'red': 0, 'yellow': 30}

        histogram_colors = histogram.get_main_colors(5)
        first_color = histogram_colors[0]
        second_color = histogram_colors[1]

        probable_color_list = []
        for histogram_color in histogram_colors:
            color_key, color_value = min(self.team_color_orientation.items(), key=lambda x: abs(histogram_color[0] - x[1]))
            if color_value not in probable_color_list:
                probable_color_list.append(color_value)

        if not self.isBuli:
            first_color = [probable_color_list[0]]#0#first_color_value
            second_color = [probable_color_list[1]] #0#second_color_value
        elif self.isBuli:
            first_color = [color_1]
            second_color = [color_2]

        self.colors_list = []
        self.colors_list.append(first_color)
        self.colors_list.append(second_color)

        image_one = cv.inRange(img_hsv, np.array([first_color[0]-15, 50, 50]), np.array([first_color[0]+15, 255, 255]))
        image_two = cv.inRange(img_hsv, np.array([second_color[0]-15, 50, 50]), np.array([second_color[0]+15, 255, 255]))

        utility.displayColor(first_color[0])
        utility.displayColor(second_color[0])

        utility.showResizedImage("TeamColorCalibration - Image One ", image_one, 0.4)
        utility.showResizedImage("TeamColorCalibration - Image Two ", image_two, 0.4)

        self.isCalibrated = True

    def count_hue_pixel(self, img, hue, offset):
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        binary_image = cv.inRange(img_hsv, np.array([hue - offset, 40, 40]), np.array([hue + offset, 255, 255]))
        pixel_count = cv.countNonZero(binary_image)
        return pixel_count
