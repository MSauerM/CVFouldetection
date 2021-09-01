from numpy import ndarray


class Frame:
    """
    Class for store information about a specific image inside a video
    ......

    Attributes
    -----------------
        _timestamp
            timestamp of the image inside the video
        _pixels
            image information
        _frameindex
            index of the image inside the video

    Methods
    -----------------
        get_pixels()
            returns the image information of the frame
        get_dimensions()
            returns the dimensions of image
        get_frame_index()
            returns the index of the frame
        get_timestamp()
            returns the timestamp of the frame

    """

    def __init__(self, timestamp: float, pixels: ndarray, frameindex: int):
        self._timestamp = timestamp
        self._pixels = pixels
        self._frameindex: int = frameindex

    def get_pixels(self):
        return self._pixels

    def get_dimensions(self):
        return self._pixels.shape[:2] # 0 is height and 1 is width

    def get_frame_index(self) -> int:
        return self._frameindex

    def get_timestamp(self):
        return self._timestamp

    def __str__(self):
        return "Index: {index}, Timestamp: {timestamp}".format(index = self.get_frame_index(),timestamp = self.get_timestamp())