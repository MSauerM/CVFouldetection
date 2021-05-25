from cv2 import cv2 as cv

import appconfig


def showResizedImage( windowname, img, scalingFactor, waitKey=None):
    if appconfig.show_debug_windows:
        height, width = img.shape[:2]
        tmpImg = cv.resize(img, (int(width * scalingFactor), int(height * scalingFactor)))
        cv.imshow(windowname, tmpImg)
        if waitKey is None:
            cv.waitKey(0)
        else:
            cv.waitKey(waitKey)
    else:
        print("Set show_debug_windows to True for getting a window here")
