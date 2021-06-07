from numpy import ndarray


class Frame():

    def __init__(self, timestamp: float, pixels: ndarray, framecount: int):
        self._timestamp = timestamp
        self._pixels = pixels
        self._framecount: int = framecount

    def getPixels(self):
        return self._pixels

    def getDimensions(self):
        return self._pixels.shape[:2] # 0 is height and 1 is width

    def getFrameCount(self) -> int:
        return self._framecount

    def getTimestamp(self):
        return self._timestamp