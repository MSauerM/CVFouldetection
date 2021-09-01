from BasicFramework.Frame import Frame
from typing import List
from CVUtility import ImageUtility as utility


class Sequence:
    """
        Class for storing sequential frame objects
        ......

        Attributes
        -----------------
            frame_list
                List of frame instances

        Methods
        -----------------
            get_frame_count()
                returns length of the frame list
            get_dimensions()
                returns the dimensions of the first frame in the sequence (same for every frame in a sequence)
            get_frames()
                returns the frame_list
            show_sequences()
                shows the frame in sequential order with CVUtility showResizedImage()-function
        """
    frame_list: List[Frame] = []

    def __init__(self, frame_list):
        self.frame_list = frame_list

    def get_frame_count(self):
        return len(self.frame_list)

    def get_dimensions(self):
        return self.frame_list[0].get_dimensions()

    def get_frames(self):
        return self.frame_list

    def show_sequence(self):
        for frame in self.frame_list:
            utility.showResizedImage("Sequenz", frame.get_pixels(), 1.0, waitKey=0)

    def __str__(self):
        return "len: {length}, first:{first}, last:{last}"\
            .format(length= self.get_frame_count(), first = self.frame_list[0], last=self.frame_list[-1])