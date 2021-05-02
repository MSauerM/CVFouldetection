from cv2 import cv2 as cv


def showResizedImage( windowname, img, scalingFactor):
    height, width = img.shape[:2]
    tmpImg = cv.resize(img, (int(width * scalingFactor), int(height * scalingFactor)))
    cv.imshow(windowname, tmpImg)
    cv.waitKey(0)
