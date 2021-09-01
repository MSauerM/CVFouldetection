import numpy as np


class BoundingBoxInformation:
    """
        Data structure for storing information about a bounding box
        ......

        Attributes
        -----------------
            _frame_index
                index of the frame, which is connected to the bounding box
            _x
                x coordinate of the bounding box (top left corner)
            _y
                y coordinate of the bounding box (top left corner)
            _w
                width of the bounding box
            _h
                height of the bounding box
            _midpoint
                calculated midpoint by adding width/2 to x and height/2 to y
        Methods
        -----------------
            get_bounds()
                returns x, y, width and height
            get_frame_index()
                returns the _frame_index
            get_midpoint()
                returns the calculated midpoint
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
