from BasicFramework.Frame import Frame


class Filter: # maybe make filter to an interface

    def __init__(self):
        print("This is the base filter")

    def filter(self, frame: Frame, preprocessed_frames=None):
        print("Filter for processing a simple frame")

    #def filter(self, frame: Frame, preprocessed_frames):
    #    print("Filter for processing a frame based on multiple already processed Frames")

