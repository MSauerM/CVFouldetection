from BasicFramework.Sequence import Sequence
from Fouldetection.BoundingBoxInformationChain import BoundingBoxInformationChain


class ContactEvent:
    sequence: Sequence = None
    bounding_box_chain: BoundingBoxInformationChain = None
    isFoul = None

    def __init__(self, sequence: Sequence, bounding_box_chain: BoundingBoxInformationChain):
        self.sequence = sequence
        self.bounding_box_chain = bounding_box_chain
        self.isFoul = False

    def __str__(self):
        #print("Here goes something with the information about a contact event")
        return "Here goes the something"

    def __repr__(self):
        return self.__str__()
