from numpy import ndarray


class Frame():

    def __init__(self, timestamp: float, pixels: ndarray, framecount: int):
        self._timestamp = timestamp
        self._pixels = pixels
        self._framecount = framecount

    def getDimensions(self):
        return self._pixels.shape[:2] # is Width or height first?

    def getFrameCount(self):
        return self._framecount

    def getTimestamp(self):
        return self._timestamp