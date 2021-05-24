from cv2 import cv2 as cv
from matplotlib import pyplot as plt
from CVUtility import ImageUtility as utility
from itertools import chain
import numpy as np

class ColorHistogram:

    _hist = None
    _main_color_list = None

    def __init__(self, img, mask=None, bins=180, range=180):
        print("HSV Color Histogram")
        # Calculate Histogram
        # cv.calcHist is faster than np.histogram
        # (up to 40x - https://docs.opencv.org/master/d1/db7/tutorial_py_histogram_begins.html)
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        #                   img,   channels, mask, histSize (180 for Hue), ranges
        utility.showResizedImage("Color Histogram Test - Image", img, 0.4)
        utility.showResizedImage("Color Histogram Test - Mask", mask, 0.4)
        self._hist = cv.calcHist([hsv_img], [0], mask, [bins], [0, range])

    def show_histogram(self):
        plt.plot(self._hist)
        plt.xlim([0, 180])
        plt.show()

    def _find_peaks(self, amount: int):
        local_peaks = []
        excluded_indices = []
        mask = np.zeros(self._hist.size, dtype=bool)
        histogram_copy = self._hist
        for i in range(amount):
            if excluded_indices:
                mask[excluded_indices] = True
                histogram_copy = np.ma.array(self._hist, mask=mask)
            value = np.amax(histogram_copy)
            index = np.where(histogram_copy == value)[0][0] # index corresponds to the hue
            local_peaks.append([index, value])
            lower_local_bound = index-15
            upper_local_bound = index+15
            local_range = None
            if upper_local_bound > 179:
                local_range = chain(range(lower_local_bound, 180), range(0,upper_local_bound-179))
            else:
                local_range = range(index-15, index +15)
            excluded_indices.extend(local_range)
        return local_peaks

    def get_main_colors(self, amount: int):
        if self._main_color_list is None:
            #print(self._hist[0])
            self._main_color_list = []

            local_peaks = self._find_peaks(amount)
            local_peaks.sort(key=lambda x:x[1], reverse=True) # Theoretically unnecessary, because local peaks are always found from big to small
            self._main_color_list = local_peaks
            #for value in self._hist:
            #    if not self._main_color_list or len(self._main_color_list) < amount:
            #        self._main_color_list.append([np.where(self._hist == value)[0], value])
            #        self._main_color_list.sort(key = lambda x:x[1], reverse=True) # sorting by the second value which is the pixelamount
            #    else:
            #        if value > self._main_color_list[-1][1]:
            #            index = np.where(self._hist == value)[0]
            #            self._main_color_list.append([index, value])
            #            self._main_color_list.sort(key=lambda x: x[1], reverse=True)
            #            del self._main_color_list[-1]
        return self._main_color_list
