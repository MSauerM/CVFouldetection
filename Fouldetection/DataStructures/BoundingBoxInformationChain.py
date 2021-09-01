from typing import List

from Fouldetection.DataStructures.BoundingBoxInformation import BoundingBoxInformation
import numpy as np


class BoundingBoxInformationChain:
    """
        Class for sequential chaining of BoundingBoxInformation instances
        ......

        Attributes
        -----------------
            chain_members: List[BoundingBoxInformation]
                list of the chained BoundingBoxInformation instances
        Methods
        -----------------
            contains(bbInformation)
                checks if the chain_members list contains the given bbInformation already
            search_for_new_chain_link(bbInformation)
                searches inside the given list (bbInformation) for a new chain link
            add(box_info)
                adds the box_info to the chain_members list
        """

    def __init__(self):
        self.chain_members: List[BoundingBoxInformation] = []

    def contains(self, bbInformation: BoundingBoxInformation):
        for link in self.chain_members:
            if bbInformation.get_frame_index() == link.get_frame_index():
                return True
            else:
                return False

    def search_for_new_chain_link(self, bbInformation: List[BoundingBoxInformation]):
        last = self.chain_members[-1]
        for info in bbInformation:
            distanceVector = (info.get_midpoint() - last.get_midpoint())
            distance = np.linalg.norm(distanceVector)
            if distance < 15:  # maxDistance
                self.add(info)
                return info

    def add(self, box_info: BoundingBoxInformation):
        self.chain_members.append(box_info)
