import cv2

from BasicFramework.Frame import Frame
from Fouldetection.Filter.Filter import Filter
from CVUtility import ImageUtility as utility
import cv2 as cv
import numpy as np


class CourtBoundsFilter(Filter):

    def __init__(self):
        super().__init__()
        print("courtBounds")

    def filter(self, frame: Frame):
        gray_img = cv.cvtColor(frame.get_pixels(), cv.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray_img, 50, 150, apertureSize=3)

        # try with Hough Lines for Line Detection
        lines = cv.HoughLines(edges, 1, np.pi/180, 200)

        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)

            x0 = a * rho
            y0 = b * rho

            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))

            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv.line(gray_img, (x1, y1), (x2,y2), (0,0,255), 2)

        utility.showResizedImage("Hough Lines", gray_img , 0.4)

        # convex Hull in Particle Filter from Single Moving Camera-Paper

