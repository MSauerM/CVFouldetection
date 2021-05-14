from BasicFramework.Frame import Frame
from Fouldetection.Filter import Filter


class CourtBoundsFilter(Filter):

    def __init__(self):
        print("courtBounds")

    def filter(self, frame: Frame):
        hsv_img = frame.getPixels()

