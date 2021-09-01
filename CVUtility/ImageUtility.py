import matplotlib.pyplot as plt
from cv2 import cv2 as cv
from matplotlib.colors import hsv_to_rgb
import numpy as np

import appconfig


def showResizedImage( windowname, img, scalingFactor, waitKey=None):
    """
    shows a resized image with the OpenCV imshow
    :param windowname: Name of the appearing window
    :param img: displayed image
    :param scalingFactor: resizing factor for the window
    :param waitKey: optional for creating automatic displaying of windows
    :return: None
    """
    if appconfig.show_debug_windows and img is not None:
        height, width = img.shape[:2]
        tmpImg = cv.resize(img, (int(width * scalingFactor), int(height * scalingFactor)))
        cv.imshow(windowname, tmpImg)
        if waitKey is None:
            cv.waitKey(0)
        else:
            cv.waitKey(waitKey)


def displayColor(hue):
    """
    draw the hue to a plot for visualizing the color of the hue
    :param hue: displayed hue color
    :return: None
    """
    if appconfig.show_debug_plots:
        color = (hue, 255, 255)
        lo_square = np.zeros((10, 10, 3))
        lo_square[:] = (color[0]/180, color[1]/255, color[2]/255)
        plt.subplot(1, 2, 1)
        rgb = hsv_to_rgb(lo_square)
        plt.imshow(rgb)
        plt.show()
