from BasicFramework.Frame import Frame
from typing import List
from CVUtility import ImageUtility as utility

class Sequence():
    frame_list = []
    # alternative would be to just save a reference to the whole framelist and set the framecount of start and ending frame
    # problem with this alternative approach is that, the image is reduced with described approaches so its not directly
    # the same frame, it is a smaller frame so frame_list to store this frames for itself is the better solution

    def __init__(self, frame_list):
        self.frame_list = frame_list

    def getFrameCount(self):
        return len(self.frame_list)


    def getDimensions(self):
        return self.frame_list[0].getDimensions()

    def showSequence(self):
        for frame in self.frame_list:
            utility.showResizedImage("Sequenz", frame, 0.4, waitKey=1)

