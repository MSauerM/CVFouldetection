import matplotlib.pyplot as plt
from cv2 import cv2 as cv
from matplotlib.colors import hsv_to_rgb
import numpy as np

import appconfig


def showResizedImage( windowname, img, scalingFactor, waitKey=None):
    if appconfig.show_debug_windows and img is not None:
        height, width = img.shape[:2]
        tmpImg = cv.resize(img, (int(width * scalingFactor), int(height * scalingFactor)))
        cv.imshow(windowname, tmpImg)
        if waitKey is None:
            cv.waitKey(0)
        else:
            cv.waitKey(waitKey)


def displayColor(hue):
    if appconfig.show_debug_plots:
        color = (hue, 255, 255)
        lo_square = np.zeros((10, 10, 3))
        lo_square[:] = (color[0]/180, color[1]/255, color[2]/255)
        plt.subplot(1, 2, 1)
        rgb = hsv_to_rgb(lo_square)
        plt.imshow(rgb)
        plt.show()
