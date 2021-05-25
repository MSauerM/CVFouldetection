

class BoundingBoxInformation:

    def __init__(self, frame_index: int, x, y, w, h):
        #print("Bounding Box")
        self._frame_index: int = frame_index
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def get_bounds(self):
        return (self._x, self._y, self._w, self._h)

    def get_frame_index(self) -> int:
        return self._frame_index
