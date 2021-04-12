

class Filter:

    def __init__(self):
        print("This is the base filter")

    def filter(self, frame):
        print("Filter for processing a simple frame")

    def filter(self, frame, preprocessed_frames):
        print("Filter for processing a frame based on multiple already processed Frames")

