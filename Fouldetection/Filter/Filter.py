from BasicFramework.Frame import Frame


class Filter: # maybe make filter to an interface
    """
    Interface for other filters
    """
    def __init__(self):
        pass

    def filter(self, frame: Frame, preprocessed_frames=None):
        print("Filter for processing a simple frame")


