import numpy as np


class BoundingBoxInformation:
    """
        Data structure for ....
        ......

        Attributes
        -----------------



        Methods
        -----------------

        """
    def __init__(self, frame_index: int, x, y, w, h):
        self._frame_index: int = frame_index
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._midpoint = np.array([self._x+self._w/2, self._y+ self._h/2])

    def get_bounds(self):
        return (self._x, self._y, self._w, self._h)

    def get_frame_index(self) -> int:
        return self._frame_index

    def get_midpoint(self):
        return self._midpoint
