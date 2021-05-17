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
        histogram.show_histogram()
        utility.showResizedImage("TeamColorCalibration - Image", img, 0.4)
        utility.showResizedImage("TeamColorCalibration - Mask", mask, 0.4)
        self.isCalibrated = True
