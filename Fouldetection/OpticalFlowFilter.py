from typing import List

import numpy as np

from BasicFramework.Frame import Frame
import CVUtility.ImageUtility as utility

from cv2 import cv2 as cv

class OpticalFlowFilter:


    def __init__(self, frame_list: List[Frame]):
        self.frame_list = frame_list


    def filter(self):

        flow_image_list = []
        for i in range(0, len(self.frame_list)-1):
            current = self.frame_list[i].getPixels()
            next = self.frame_list[i+1].getPixels()

            hsv = np.zeros_like(current)
            hsv[..., 1] = 255

            current = cv.cvtColor(current, cv.COLOR_BGR2GRAY)
            next = cv.cvtColor(next, cv.COLOR_BGR2GRAY)



            flow = cv.calcOpticalFlowFarneback(current,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

            mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
            #hsv[...,0] = ang * (180 / np.pi / 2)
            #hsv[...,2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
            hsv[:,:,0] = ang * (180 / np.pi / 2)
            hsv[:,:,2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)

            bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
            flow_image_list.append(bgr)

        for bgr in flow_image_list:
            utility.showResizedImage("Flow", bgr, 0.4)