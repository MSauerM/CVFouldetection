from numpy import ndarray


class Frame():

    def __init__(self, timestamp: float, pixels: ndarray, framecount: int):
        self._timestamp = timestamp
        self._pixels = pixels
        self._framecount = framecount
