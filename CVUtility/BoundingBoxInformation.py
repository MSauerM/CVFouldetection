

class BoundingBoxInformation:

    def __init__(self, frame_index, x, y, w, h):
        #print("Bounding Box")
        self._frame_index = frame_index
        self._x = x
        self._y = y
        self._w = w
        self._h = h
