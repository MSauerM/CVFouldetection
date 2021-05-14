from cv2 import cv2 as cv


def showResizedImage( windowname, img, scalingFactor, waitKey=None):
    height, width = img.shape[:2]
    tmpImg = cv.resize(img, (int(width * scalingFactor), int(height * scalingFactor)))
    cv.imshow(windowname, tmpImg)
    if waitKey is None:
        cv.waitKey(0)
    else:
        cv.waitKey(waitKey)

