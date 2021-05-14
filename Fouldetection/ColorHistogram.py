from cv2 import cv2 as cv
from matplotlib import pyplot as plt

class ColorHistogram:

    _hist = None

    def __init__(self, img, mask=None, bins=180, range=180):
        print("HSV Color Histogram")
        # Calculate Histogram
        # cv.calcHist is faster than np.histogram
        # (up to 40x - https://docs.opencv.org/master/d1/db7/tutorial_py_histogram_begins.html)
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        #                   img,   channels, mask, histSize (180 for Hue), ranges
        self._hist = cv.calcHist([hsv_img], [0], mask, [bins], [0, range])

    def show_histogram(self):
        plt.plot(self._hist)
        plt.xlim([0,180])
        plt.show()


    def get_main_colors(self):
        return None
