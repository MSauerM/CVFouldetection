import numpy as np

from BasicFramework.Frame import Frame
from Fouldetection.DataStructures.BoundingBoxInformation import BoundingBoxInformation

import cv2 as cv
import CVUtility.ImageUtility as utility
from Fouldetection.Filter.Filter import Filter


class PlayerFilter(Filter):
    """
        Class for filtering the necessary bounding box information and edges
        ......

        Attributes
        -----------------

        Methods
        -----------------
            filter(frame, preprocessed_frames)
                processes the given frame in regards to the information of the preprocessed_frames
                to get BoundingBoxInformation instances and a edge image
        """
    def __init__(self):
        super().__init__()

    def filter(self, frame: Frame, preprocessed_frames = None):
        # canny Edge detection
        img = frame.get_pixels()
        frame_hsv = cv.cvtColor(frame.get_pixels(), cv.COLOR_BGR2HSV)

        kernel = np.ones( (5,5), np.uint8)
        greater_kernel = np.ones((11,11), np.uint8)

        dilated_grassfilteredFrame = cv.dilate(preprocessed_frames[0], kernel, iterations=3)
        utility.showResizedImage("Player Filter - Dilated Grass Filtered", dilated_grassfilteredFrame, 0.4)

        (contours, hierarchy) = cv.findContours(dilated_grassfilteredFrame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


        player_img = cv.bitwise_and(frame.get_pixels(), frame.get_pixels(), mask=dilated_grassfilteredFrame)

        masked_img = cv.bitwise_and(img, img, mask= preprocessed_frames[1])

        edges = cv.Canny(masked_img, 150, 200)
        edges = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel=kernel, iterations=1)
        edges = cv.morphologyEx(edges, cv.MORPH_OPEN, kernel=kernel, iterations=3)

        utility.showResizedImage("Player Filter - Edges", edges, 0.4)

        boundingBoxInformation_list = []

        font = cv.FONT_HERSHEY_PLAIN

        for c in contours:
            x, y, w, h = cv.boundingRect(c)
            if ( (w > 20 and h > 20)  and (w < 450 and h < 450)):
                boundingBoxInformation_list.append(BoundingBoxInformation(frame.get_frame_index(), x, y, w, h))

        utility.showResizedImage("Player Filter - Result", img, 0.4)
        return boundingBoxInformation_list, edges
