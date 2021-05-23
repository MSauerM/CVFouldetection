import cv2

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

        histogram.show_histogram()
        utility.showResizedImage("TeamColorCalibration - Image", img, 0.4)
        utility.showResizedImage("TeamColorCalibration - Mask", mask, 0.4)
        utility.showResizedImage("TeamColorCalibration - Fusion", cv2.bitwise_and(img, img, mask= mask), 0.4)
        self.isCalibrated = True
